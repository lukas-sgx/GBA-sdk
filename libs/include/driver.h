/* Device drivers and driver cycles
A driver is any part of the program that manages some piece of hardware */

typedef struct {
  /* Driver name */
  char const *name;
  /* Initialize the hardware for the driver . Usually installs
  interrupt handlers and configures registers . May be NULL . */
  void (*configure)(void);
} wired_drv_t;

/* WIRED _ DECLARE _ DRIVER () : Declare a driver to the kernel
Use this macro to declare a driver by passing it the name of a
` struct wired _ driver ` structure . This macro moves the structure to the
`. wired . drivers .* ` sections , which are automatically traversed at
startup .
The level argument represents the priority level : lower numbers mean
that drivers will be loaded sooner . This numbering allows a primitive
form of dependency for drivers . You need to specify a level which is
strictly higher than the level of all the drivers you depend on . */
#define WIRED_DECLARE_DRIVER(level, name, ...) \
    __attribute__((used, section(".wired.drivers." #level))) \
    static const wired_drv_t __wired_drv_##name = { __VA_ARGS__ }

/* Drivers in order of increasing priority level , provided by linker script */
extern wired_drv_t __wired_drivers[];
/* End of array ; see also wired _ driver _ count () */

extern wired_drv_t __wired_drivers_end[];
/* Number of drivers in the ( wired _ drivers ) array */

#define wired_driver_count() \
  ((wired_drv_t *)&__wired_drivers_end - (wired_drv_t *)&__wired_drivers)
