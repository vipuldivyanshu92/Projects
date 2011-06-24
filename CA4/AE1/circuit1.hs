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
ireg :: Clocked a => a -> a -> a
ireg invert clear = r
    where r = dff (and2 (inv clear) (xor2 invert r))

{-
 - Define a simple 4 bits counter using the inverting register defined above,
 -  this circuit could be implemented using a circuit generator to support a
 -  counter of size k.
 -}
counter4 :: Clocked a => a -> a -> [a]
counter4 inc clear = [q3, q2, q1, q0]
    where
        q0 = ireg inc clear
        q1 = ireg q0 clear
        q2 = ireg (and2 q0 q1) clear
        q3 = ireg (and3 q0 q1 q2) clear

{-
 - G1 > G2 > G3 > A1 > R1 > R2 > R3 > R4 > A2 >>
 -
 -}
traffic1 :: Clocked a => [a]
traffic1 = [green, amber, red]
    where
        [q3, q2, q1, q0] = counter4 one q3

        green = inv (or2 amber red)             -- Green if not red or amber
        amber = or2 (and3 q0 q1 (inv q2)) q3    -- Amber if counter is 3 or 8
        red = q2                                -- Red if counter is 4, 5, 6 or 7

{-
 - <--
 - G1 > A1 > R1 > R2 > R3 > A2 >>
 -
 - State Green 1 is persistent, the counter stops incrementing
 -  while push button is not set
 -}
traffic2 :: Clocked a => a -> [a]
traffic2 request = [green, amber, red, walk, wait]
    where
        ctl_pb = or2 request (inv green)
        st_amber2 = and2 q0 q2

        [q3, q2, q1, q0] = counter4 ctl_pb st_amber2

        green = inv (or4 q0 q1 q2 q3)           -- Green if counter is 0
        amber = and3 (inv q3) q0 (inv q1)       -- Amber if counter is 1 or 5
        red = inv (or2 green amber)             -- Red if not green and amber
        walk = red                              -- Walk if red
        wait = inv walk                         -- Wait if not walk

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
        
        st_green5 = and4 (inv q0) (inv q1) q2 (inv q3)  -- State green5 when counter is 4
        st_amber1 = and4 q0 (inv q1) q2 (inv q3)        -- State amber1 when counter is 5

        reg_pb = reg1 (or2 st_amber1 request) request   -- Store/Clear the value of the push button

        ctl_inc = or2 reg_pb (inv st_green5)            -- Increment if pushbutton is pressed or not in green 5
        ctl_reset = and2 q3 q0                          -- Reset when counter is 9
        
        [q3, q2, q1, q0] = counter4 ctl_inc ctl_reset

        green = or2 (and2 (inv q2) (inv q3)) (and3 (inv q1) (inv q0) (inv q3)) -- Green if counter 0..4
        amber = and2 (xor2 q3 q2) (and2 (inv q1) q0)    -- Amber if counter is 5 or 9
        red = inv (or2 green amber)                     -- Red if not green and amber
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
