#ifndef ALIGN_H
    #define ALIGN_H

/* Packed structures . I require explicit alignment because if it 's
unspecified , GCC cannot optimize access size , and reads to memory - mapped
I/O with invalid access sizes silently fail - honestly you don 't want
this to happen */
#define WPACKED(x) __attribute__((packed, aligned(x)))

/* Giving a type to padding bytes is misguiding , let 's hide it in a macro */
#define pad_nam2( c) _ ## c
#define pad_name(c) pad_nam2(c)
#define pad(bytes) u8 pad_name(__COUNTER__) [bytes]

/* word _ union () - union between an u 16 ' word ' element and a bit field */
#define word_union(name, fields) \
    union { \
        uint16_t word; \
        struct { fields } WPACKED(2); \
    } WPACKED(2) name
#endif