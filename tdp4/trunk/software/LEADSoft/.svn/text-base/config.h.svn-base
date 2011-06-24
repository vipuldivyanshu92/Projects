/* 
 * File:   config.h
 * Author: adraen
 *
 * Created on 15 April 2011, 15:02
 */

#ifndef CONFIG_H
#define	CONFIG_H

#ifdef	__cplusplus
extern "C" {
#endif

typedef void* config_t;

config_t config_init();
int config_save(config_t config);
int config_release(config_t config);
int config_get_dword(config_t config, char *name, int *value);
int config_get_string(config_t config, char *name, char **value);
int config_set_dword(config_t config, char *name, int value);
int config_set_string(config_t config, char *name, char *value);

#ifdef	__cplusplus
}
#endif

#endif	/* CONFIG_H */

