#include "functions.h"
#include "driver/spi_slave.h"
#include "driver/gpio.h"
#include "esp_err.h"
#include <stdint.h>
#include <string.h>
#include <stdio.h>

last_trans_info_t last_trans = {.recv_buffer_pointer = NULL, .size = 0};

mp_obj_t spi_slave_init(mp_uint_t n_args, const mp_obj_t *args)
{
	int mosi, miso, sclk, cs, dma_channel;
	esp_err_t result;
	mosi = mp_obj_get_int(args[0]);
	miso = mp_obj_get_int(args[1]);
	sclk = mp_obj_get_int(args[2]);
	cs = mp_obj_get_int(args[3]);
	dma_channel = 0;

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
        .flags=0
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
    // if(last_trans.recv_buffer_pointer != NULL)
    //     free(last_trans.recv_buffer_pointer);
	result = spi_slave_free(HSPI_HOST);
	if(result==ESP_OK)
    	return mp_const_true;
    else
    	return mp_const_false;
}

mp_obj_t spi_slave_enable_transaction(mp_obj_t sendbuf_obj)
{
	spi_slave_transaction_t transaction;
    esp_err_t result;
    mp_uint_t num_transfers;
    mp_obj_t *transfers_obj_array;
    mp_obj_get_array(sendbuf_obj, &num_transfers, &transfers_obj_array);
    uint8_t *sendbuf = (uint8_t*)malloc(num_transfers);
    uint8_t *recvbuf = (uint8_t*)malloc(num_transfers);
    uint8_t * sendbuf_aux = sendbuf;
    if(last_trans.recv_buffer_pointer != NULL)
        free(last_trans.recv_buffer_pointer);
    last_trans.recv_buffer_pointer = recvbuf;
    last_trans.size = num_transfers;
    for(int i = 0; i < num_transfers; ++i)
    {
        *sendbuf_aux = (uint8_t)mp_obj_get_int(*transfers_obj_array);   
        sendbuf_aux++;
        transfers_obj_array++;   
    } 
    memset(&transaction, 0, sizeof(transaction)); 
    transaction.length=num_transfers*8;
    transaction.tx_buffer=sendbuf;
    transaction.rx_buffer=recvbuf;
    result = spi_slave_transmit(HSPI_HOST, &transaction, portMAX_DELAY);
    if (result == ESP_OK)
    {
        printf("Transaction ok\n");
        free(sendbuf);
        return mp_obj_new_bytearray(num_transfers, recvbuf);
    }
    else   
    {
        printf("Transaction not ok");
        return mp_const_false;
    }
}

// mp_obj_t spi_slave_enable_transaction(mp_obj_t sendbuf_obj,  mp_obj_t recvbuf_obj)
// {
//     spi_slave_transaction_t transaction;
//     esp_err_t result;

//     mp_buffer_info_t src;
//     mp_get_buffer_raise(sendbuf_obj, &src, MP_BUFFER_READ);
//     mp_buffer_info_t dest;
//     mp_get_buffer_raise(recvbuf_obj, &dest, MP_BUFFER_WRITE);
//     if (src.len != dest.len) {
//         mp_raise_ValueError("buffers must be the same length");
//     }
//     memset(&transaction, 0, sizeof(transaction)); 
//     transaction.length=src.len*8;
//     transaction.tx_buffer=src.buf;
//     transaction.rx_buffer=dest.buf;
//     result = spi_slave_transmit(HSPI_HOST, &transaction, portMAX_DELAY);
//     if (result == ESP_OK)
//     {
//         printf("Transaction aconteceu com sucesso\n");
//         return mp_const_true;
//     }
//     else   
//     {
//         printf("Transaction esmerdou");
//         return mp_const_false;
//     }
// }

mp_obj_t spi_slave_get_received_buffer()
{
    return mp_obj_new_bytearray(last_trans.size, last_trans.recv_buffer_pointer);
}
