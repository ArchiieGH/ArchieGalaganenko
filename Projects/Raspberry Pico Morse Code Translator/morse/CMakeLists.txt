add_executable(morse_code
        morse_code.c
        )

# pull in common dependencies
target_link_libraries(morse_code pico_stdlib)

# create map/bin/hex file etc.
pico_add_extra_outputs(morse_code)


