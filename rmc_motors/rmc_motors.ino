bool stopAll = false;

#include "RMCKangaroo.hpp"
RMCKangaroo k(Serial3);


/*

[
    Command: uint8_t
    Device: uint8_t
    Val1: int8_t
    Val2: int8_t
    Checksum: uint8_t
]

*/

void setup() {

    k.begin();
    k.motors->drive(10, 100);
}


void loop() {

    // run mots if enabled
    if (!stopAll)
        k.loop();


}
