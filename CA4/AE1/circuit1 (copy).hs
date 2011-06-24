module Main where

import HydraLib
import HydraLib.StandardCircuits

{-
 - clear | invert || r 
 --------------------------
 -   1        x   || 0
 -   0        0   || r
 -   0        1   || inv r
 -}
block :: Clocked a => a -> a -> a
block invert clear = r
    where r = dff (and2 (inv clear) (xor2 invert r))

counter4 :: Clocked a => a -> a -> [a]
counter4 inc clear = [q3, q2, q1, q0]
    where
        q0 = block inc clear
        q1 = block q0 clear
        q2 = block (and2 q0 q1) clear
        q3 = block (and3 q0 q1 q2) clear

traffic1 :: Clocked a => [a]
traffic1 = [green, amber, red]
    where
        [q3, q2, q1, q0] = counter4 one q3
        green = inv (or2 amber red)
        amber = or2 (and3 q0 q1 (inv q2)) q3
        red = q2

traffic2 :: Clocked a => a -> [a]
traffic2 request = [green, amber, red, walk, wait]
    where
        [q3, q2, q1, q0] = counter4 (or2 request (and2 (inv green) (inv request))) (and2 q0 q2)
        green = inv (or4 q0 q1 q2 q3)
        amber = and3 (inv q3) q0 (inv q1)
        red = inv (or2 green amber)
        walk = red
        wait = inv walk

{-
 -                     <--
 - G1 > G2 > G3 > G4 > G5 > A1 > R1 > R2 > R3 > A2 >>
 - 
 - State Green 5 is persistent, the counter stops incrementing
 -  while push button is not set
 - 
 - In State Amber 1 the push button register is cleared
 -}
traffic3 :: Clocked a => a -> [a]
traffic3 request = [green, amber, red, walk, wait]
    where
        
        st_green5 = and4 (inv q0) (inv q1) q2 (inv q3)
        st_amber1 = and4 q0 (inv q1) q2 (inv q3)        

        reg_pb = reg1 (or2 st_amber1 request) (mux1 request zero one)

        ctl_inc = or2 reg_pb (and2 (inv st_green5) (inv reg_pb))
        ctl_reset = and2 q3 q0
        
        [q3, q2, q1, q0] = counter4 ctl_inc ctl_reset

        green = or2 (and2 (inv q2) (inv q3)) (and3 (inv q1) (inv q0) (inv q3))
        amber = and2 (xor2 q3 q2) (and2 (inv q1) q0)
        red = inv (or2 green amber)
        walk = red
        wait = inv walk

sim :: [[Int]] -> IO ()
sim input =
    do runThroughInput input output
    where
        p = getbit input 0
        -- [green, amber, red] = traffic1
        -- [green, amber, red, walk, wait] = traffic2 p
        [green, amber, red, walk, wait] = traffic3 p
        output = [bit green, bit amber, bit red]

main :: IO ()
main =
    do sim input1

input1 = 
   [[0],
    [0],
    [1],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [1],
    [0],
    [0]]
