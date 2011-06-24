/* 
 * File:   can_packets.h
 * Author: adraen
 *
 * Created on 20 April 2011, 14:44
 */

#ifndef CAN_PACKETS_H
#define	CAN_PACKETS_H

#ifdef	__cplusplus
extern "C" {
#endif

#define FL_WHEEL_SPEED          0x1E1
#define FR_WHEEL_SPEED          0x1E2
#define RL_WHEEL_SPEED          0x1E3
#define RR_WHEEL_SPEED          0x1E4

#define GPS_SPEED               0x7A1
#define ROAD_SPEED              0x1E0



#define GEAR_CHANGE             0x1A0
#define ENGINE_REVS             0x0E0
#define FUEL_LEVEL              0x360
#define OIL_TEMP                0x260
#define COOLANT_TEMP            0x2E0
#define GEAR_SHIFT_CHARGE_STATE 0x1A5
#define ENGINE_TEMP_S1          0x220
#define ENGINE_TEMP_S2          0x221
#define ENGINE_TEMP_S3          0x222
#define ENGINE_TEMP_S4          0x223


#define SOURCE_ROAD_SPEED          0
#define SOURCE_WHEEL_SPEED         1
#define SOURCE_GPS_SPEED           2

    
#ifdef	__cplusplus
}
#endif

#endif	/* CAN_PACKETS_H */

