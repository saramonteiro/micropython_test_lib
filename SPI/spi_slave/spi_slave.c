#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "py/obj.h"
#include "py/runtime.h"
#include "functions.h"

STATIC MP_DEFINE_CONST_FUN_OBJ_2(spi_slave_write_on_registers_obj, spi_slave_write_on_registers);
STATIC MP_DEFINE_CONST_FUN_OBJ_2(spi_slave_read_registers_obj, spi_slave_read_registers);
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(spi_slave_init_obj, 4, 4, spi_slave_init);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(spi_slave_free_bus_obj, spi_slave_free_bus);
STATIC MP_DEFINE_CONST_FUN_OBJ_3(spi_slave_enable_transfers_obj, spi_slave_enable_transfers);
STATIC MP_DEFINE_CONST_FUN_OBJ_1(spi_slave_set_register_pointer_obj, spi_slave_set_register_pointer);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(spi_slave_disable_transfers_obj, spi_slave_disable_transfers);


STATIC const mp_rom_map_elem_t spi_slave_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_spi_slave) },
    { MP_ROM_QSTR(MP_QSTR_write_on_registers), MP_ROM_PTR(&spi_slave_write_on_registers_obj) },
    { MP_ROM_QSTR(MP_QSTR_read_registers), MP_ROM_PTR(&spi_slave_read_registers_obj) }, 
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&spi_slave_init_obj) }, 
    { MP_ROM_QSTR(MP_QSTR_free_bus), MP_ROM_PTR(&spi_slave_free_bus_obj) }, 
    { MP_ROM_QSTR(MP_QSTR_enable_transfers), MP_ROM_PTR(&spi_slave_enable_transfers_obj) },  
    { MP_ROM_QSTR(MP_QSTR_set_register_pointer), MP_ROM_PTR(&spi_slave_set_register_pointer_obj) },
    { MP_ROM_QSTR(MP_QSTR_disable_transfers), MP_ROM_PTR(&spi_slave_disable_transfers_obj) },    
};
STATIC MP_DEFINE_CONST_DICT(spi_slave_module_globals, spi_slave_module_globals_table);

const mp_obj_module_t spi_slave_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&spi_slave_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_spi_slave, spi_slave_user_cmodule, MODULE_SPI_SLAVE_ENABLED);
