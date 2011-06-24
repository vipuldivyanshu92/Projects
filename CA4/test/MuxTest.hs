module Main where

{- MuxTest.hs --- test cases for mux1 and mux1w, which are defined in
HydraLib.StandardCircuits.  To compile and run:
  ghc --make MuxTest
  ./MuxTest
-}

import HydraLib
import HydraLib.StandardCircuits

main :: IO ()
main =
  do run_mux1 mux1_testdata
     run_mux1w mux1w_testdata


------------------------------------------------------------------------
-- Testing the mux1 circuit

{- The mux1 circuit takes three bit inputs, c, x, y.  The c input is a
control that selects either x (if c=0) or y (if c=1), and the selected
input is placed on the output signal. -}

mux1_testdata :: [[Int]]
mux1_testdata =
------------
--  c  x  y
------------
  [[0, 0, 0],
   [0, 0, 1],
   [0, 1, 0],
   [0, 1, 1],
   [1, 0, 0],
   [1, 0, 1],
   [1, 1, 0],
   [1, 1, 1]]

run_mux1 :: [[Int]] -> IO ()
run_mux1 input =
  do putStrLn "\nrun_mux1"
     runThroughInput input output
  where
    c = getbit input 0
    x = getbit input 1
    y = getbit input 2
    q = mux1 c x y
    output =
      [string "c=", bit c,
       string "  x=", bit x,
       string "  y=", bit y,
       string "  output = ", bit q]

------------------------------------------------------------------------
-- Testing the mux1w circuit

{- The mux1w circuit is similar to mux1, except the data inputs and
the output are words rather than bits. -}

mux1w_testdata =
------------
--  c  x  y
------------
  [[0,  39,  47],
   [1,  39,  47],
   [0,   1,   0],
   [0, 201,  54],
   [1,  19, 243]]

run_mux1w :: [[Int]] -> IO ()
run_mux1w input =
  do putStrLn "\nrun_mux1w"
     runThroughInput input output
  where
    c = getbit input 0
    x = getbin 16 input 1
    y = getbin 16 input 2
    q = mux1w c x y
    output =
      [string "c=", bit c,
       string "  x =", bindec 4 x,
       string "  y =", bindec 4 y,
       string "  output = ", bindec 4 q]
