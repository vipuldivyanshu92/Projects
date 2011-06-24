library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

---
-- Mapper Entity definition based on SMSPower.org informations
-- Sources:
--		http://www.smspower.org/forums/viewtopic.php?t=2054	  
--		http://www.smspower.org/Development/GGCartridge		 
--		http://www.smspower.org/Development/Mappers
---
entity MAPPER_entity is
	port(	A_in: in std_logic_vector(15 downto 0);
		 	D_in: in std_logic_vector(7 downto 0);
			CE, WR, ROM_out, RAM_out): in std_logic;
			A_out: out std_logic_vector(18 downto 0)		
	);
end MAPPER_entity;

architecture MAPPER_behaviour of MAPPER_entity is
begin
	
	process(CE)
	begin		
		
	end process;
	
	-- Change the output address with respect to the input address, Chip Enable and Write
	--	CE, WR are active low
	process(A_in, CE, WR)	
		-- Select rom block for each page
		variable page0: unsigned(7 downto 0) := x"00";
		variable page1: unsigned(7 downto 0) := x"01";
		variable page2: unsigned(7 downto 0) := x"02";
	begin				
		if CE='0' then  		-- CE is active low
			-- ROM is in write mode
			if WR='0' then		-- WR is active low
				case A_in is	   
					-- MAP the SRAM
					when x"FFFC" =>
						
					-- MAP nth 16kB bank in page 0, the first 1k is not mapped (static segment)
					when x"FFFD" =>
						page0 := unsigned(D_in);
					-- MAP nth 16kB bank in page 1
					when x"FFFE" =>
						page1 := unsigned(D_in);
					-- MAP nth 16kB bank in page 2
					when x"FFFF" =>
						page2 := unsigned(D_in);
					when others =>
						-- Do nothing
				end case;
			
			-- ROM is in read mode
			else
				if (unsigned(A_in) >= x"0400" and unsigned(A_in) < x"4000") then 		   
					A_out <= std_logic_vector(shift_left(resize(page0, 19), 14) + unsigned(A_in));
				elsif (unsigned(A_in) >= x"4000" and unsigned(A_in) < x"8000") then
					A_out <= std_logic_vector(shift_left(resize(page1, 19), 14) + unsigned(A_in) - x"4000");
				elsif (unsigned(A_in) >= x"8000" and unsigned(A_in) < x"C000") then
					A_out <= std_logic_vector(shift_left(resize(page2, 19), 14) + unsigned(A_in) - x"8000");
				end if;
			end if;
		else
			A_out <= "0000000000000000000";
		end if;
	end process;
	
end MAPPER_behaviour;
	