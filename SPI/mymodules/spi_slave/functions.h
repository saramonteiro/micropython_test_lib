#include "py/obj.h"
#include "py/runtime.h"
#include <stdint.h>

typedef struct last_trans_info
{
	uint8_t * recv_buffer_pointer;
	uint8_t size;
}last_trans_info_t;

mp_obj_t spi_slave_init(mp_uint_t, const mp_obj_t *);
mp_obj_t spi_slave_free_bus(void);
mp_obj_t spi_slave_enable_transaction(mp_obj_t);
mp_obj_t spi_slave_get_received_buffer();

