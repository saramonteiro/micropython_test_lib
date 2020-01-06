#include "functions.h"
#include "driver/spi_slave.h"
#include "driver/gpio.h"
#include "freertos/task.h"
#include "esp_err.h"
#include <stdint.h>
#include <string.h>
#include <stdio.h>


#define STACK_SIZE 8192
#define DUMMY 0x00
#define BUFFER_SIZE 1
#define READ_WO_REG 1
#define WRITE_WO_REG 2
#define READ_W_REG 3
#define WRITE_W_REG 4


uint8_t registers[256] = {0};
uint8_t send_buf, reg_pointer = 0, flag_first_time = 0, received =0;
WORD_ALIGNED_ATTR char sendbuf[1]=""; 
WORD_ALIGNED_ATTR char recvbuf[1]="";
TaskHandle_t xHandle = NULL;
Case_config_t my_case;


mp_obj_t spi_slave_write_on_registers(mp_obj_t address_obj, mp_obj_t values_obj)
{
	int address = mp_obj_get_int(address_obj);
	mp_uint_t array_len;
	mp_obj_t *array;
	mp_obj_get_array(values_obj, &array_len, &array);  
	for (int i = address; i < address+array_len; ++i)
	{
		registers[i] = mp_obj_get_int(*array);
		array++;
	}
    return mp_obj_new_int_from_uint(array_len);
}

mp_obj_t spi_slave_read_registers(mp_obj_t address_obj, mp_obj_t len_obj)
{
	int address = mp_obj_get_int(address_obj);
	int len = mp_obj_get_int(len_obj);
    return mp_obj_new_bytearray((size_t)len, &registers[address]);
}


//Called after transaction is sent/received. 
void my_post_transaction_callback(spi_slave_transaction_t *trans) 
{
    received = (uint8_t)recvbuf[0]; 
    switch (my_case.trans_case)
    {
    	// case RDWT_W_REG:
	    	// if (received != DUMMY) //Indicate Write or read reg OR Indicate value to be written
	    	// {
	    	// 	if (flag = 0) //Register
	    	// 	{
		    // 		flag = 1;
	    	// 		reg_pointer = received;
	    	// 	}
	    	// 	else  //Value to be written
	    	// 	{

	    	// 	}

	    	// }
	    	// else //received = DUMMY
	    	// {
	    	// 	reg_pointer++;	
	    	// 	flag = 0;
	    	// }
    	case READ_W_REG:
    		if (received != DUMMY)
    			reg_pointer = received;
    		else
    			reg_pointer++;
    		break;
    	case WRITE_W_REG:
    		if (flag_first_time == 0)
    		{
    			reg_pointer = received;
    			flag_first_time = 1;
    		}
    		else
    		{
    			registers[reg_pointer] = received;
    			reg_pointer++;
    		}
    		break;
    	case READ_WO_REG:
    		reg_pointer++;
    		break;
    	case WRITE_WO_REG:
    		registers[reg_pointer] = received;
    		reg_pointer++;
    		break;
    	default:
    		break;
    }
}

mp_obj_t spi_slave_init(mp_uint_t n_args, const mp_obj_t *args)
{
	int mosi, miso, sclk, cs, dma_channel;
	esp_err_t result;
	mosi = mp_obj_get_int(args[0]);
	miso = mp_obj_get_int(args[1]);
	sclk = mp_obj_get_int(args[2]);
	cs = mp_obj_get_int(args[3]);
	dma_channel = 2;

    //Configuration for the SPI bus
    spi_bus_config_t buscfg={
        .mosi_io_num=mosi,
        .miso_io_num=miso,
        .sclk_io_num=sclk,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
    };

    //Configuration for the SPI slave interface
    spi_slave_interface_config_t slvcfg={
        .mode=0,
        .spics_io_num=cs,
        .queue_size=1,
        .flags=0,
        .post_trans_cb=my_post_transaction_callback
    };

    //Enable pull-ups on SPI lines so we don't detect rogue pulses when no master is connected.
    gpio_set_pull_mode(mosi, GPIO_PULLUP_ONLY);
    gpio_set_pull_mode(sclk, GPIO_PULLUP_ONLY);
    gpio_set_pull_mode(cs, GPIO_PULLUP_ONLY);

    //Initialize SPI slave interface
    result=spi_slave_initialize(HSPI_HOST, &buscfg, &slvcfg, dma_channel);
    if(result==ESP_OK)
    	return mp_const_true;
    else
    	return mp_const_false;
}

mp_obj_t spi_slave_free_bus()
{
	esp_err_t result;
	flag_first_time = 0;
	result = spi_slave_free(HSPI_HOST);
	if(result==ESP_OK)
    	return mp_const_true;
    else
    	return mp_const_false;
}

mp_obj_t spi_slave_set_register_pointer(mp_obj_t address_obj)
{
	reg_pointer = mp_obj_get_int(address_obj);
	return mp_const_none; 
}

void vTaskSPI(void * pvParameters)
{
	spi_slave_transaction_t transaction;
	spi_slave_transaction_t *ret_trans;
	int iteration, transfer;
	memset(&transaction, 0, sizeof(transaction)); 
	if (my_case.trans_case == READ_WO_REG || my_case.trans_case == WRITE_WO_REG)
	{
		for (iteration = 0; iteration < my_case.iterations; ++iteration)
		{
			for (transfer = 0; transfer < my_case.transfers_per_iteration; ++transfer)
			{
				send_buf = registers[reg_pointer];
				//memset(recvbuf, 0xA5, BUFFER_SIZE);
		        memset(sendbuf, send_buf, BUFFER_SIZE);
		        transaction.length=BUFFER_SIZE*8;
		        transaction.tx_buffer=sendbuf;
		        transaction.rx_buffer=recvbuf;
		        spi_slave_queue_trans(HSPI_HOST, &transaction, portMAX_DELAY);
		        printf("queue_trans\n");
		        spi_slave_get_trans_result(HSPI_HOST, &ret_trans, portMAX_DELAY);
		        printf("queue_trans_result\n");
		        printf("Received %d\n", received);
	    	}
    		reg_pointer-=my_case.transfers_per_iteration;
		}
		printf("Transaction Completed!\n");
		vTaskDelete(xHandle);
	}
	else
	{
		for (transfer = 0; transfer < my_case.transfers_per_iteration; ++transfer)
		{
				send_buf = registers[reg_pointer];
				//memset(recvbuf, 0xA5, BUFFER_SIZE);
		        memset(sendbuf, send_buf, BUFFER_SIZE);
		        transaction.length=BUFFER_SIZE*8;
		        transaction.tx_buffer=sendbuf;
		        transaction.rx_buffer=recvbuf;
		        spi_slave_queue_trans(HSPI_HOST, &transaction, portMAX_DELAY);
		        printf("queue_trans\n");
		        spi_slave_get_trans_result(HSPI_HOST, &ret_trans, portMAX_DELAY);
		        printf("queue_trans_result\n");
		        printf("Received %d\n", received);
		}
		flag_first_time = 0;
		reg_pointer-=my_case.transfers_per_iteration;
		printf("Transaction Completed!\n");
		vTaskDelete(xHandle);
	}

}

mp_obj_t spi_slave_enable_transfers(mp_obj_t case_obj, mp_obj_t arg1_obj, mp_obj_t arg2_obj)
{

	my_case=(Case_config_t){
		.trans_case = mp_obj_get_int(case_obj),
		.iterations = mp_obj_get_int(arg1_obj),
		.transfers_per_iteration = mp_obj_get_int(arg2_obj),
	};
	xTaskCreate( vTaskSPI, "Task SPI", STACK_SIZE, NULL, 2, &xHandle);
	if (xHandle != NULL)
		return mp_const_true;	
	else
		return mp_const_false;

}

mp_obj_t spi_slave_disable_transfers()
{
	flag_first_time = 0;
	if (xHandle != NULL)
	{
		vTaskDelete(xHandle);
	}
	return mp_const_none; 
}