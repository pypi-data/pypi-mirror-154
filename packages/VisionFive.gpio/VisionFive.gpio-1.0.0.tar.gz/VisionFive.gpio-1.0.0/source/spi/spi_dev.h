#ifndef __SPI_DEV_H__
#define __SPI_DEV_H__

extern int spi_setmode(int speed, int mode, int bits);
extern int spi_transfer(char *data, int len);
extern int spi_getdev(char *dev);
extern int spi_freedev(void);

#endif
