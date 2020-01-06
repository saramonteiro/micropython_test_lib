#include "py/obj.h"
#include "py/runtime.h"
#include <stdint.h>
extern uint8_t registers[256];
extern TaskHandle_t xHandle;
typedef struct Case_config_t Case_config_t; 

struct Case_config_t{
	int trans_case, iterations, transfers_per_iteration;
};

mp_obj_t spi_slave_write_on_registers(mp_obj_t , mp_obj_t );
mp_obj_t spi_slave_read_registers(mp_obj_t, mp_obj_t );
mp_obj_t spi_slave_init(mp_uint_t, const mp_obj_t *);
mp_obj_t spi_slave_free_bus(void);
mp_obj_t spi_slave_enable_transfers(mp_obj_t, mp_obj_t, mp_obj_t);
mp_obj_t spi_slave_set_register_pointer(mp_obj_t);
mp_obj_t spi_slave_disable_transfers(void);
