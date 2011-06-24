import SRP6
import convertool

srp = SRP6.SRP6()
srp.set_I('EOWAMIR')
srp.set_P('N3YL9RL5WOW')

srp.set_g(7)
srp.set_N(convertool.strToInt('\xb7\x9b>*\x87\x82<\xab\x8f^\xbf\xbf\x8e\xb1\x01\x08SP\x06)\x8b[\xad\xbd[S\xe1\x89^dK\x89'[::-1]))
srp.set_s(convertool.strToInt('5\xc6\xbbUe..\x18\xf2\x82LH6\xb8\x83\xaa\x00\x8b\xc39$\xe7\xcfD\xee&._\x92H#\xf2'[::-1]))
srp.set_B(convertool.strToInt("""\xa5z\x12>Q,\x0f\xf4"\xf2x\x85\x19.\x1a\x10Nf-\xf3K8c\xd2\xa7\xf2\xf8E\xce\x18uZ"""[::-1]))
srp.set_a(3092303949206411601731613007819148364058541661)

srp.calculate_x()
print('x', srp.get_x())
srp.calculate_A()
print('A', srp.get_A())
print('B', srp.get_B())
srp.calculate_v()
print('v', srp.get_v())
srp.calculate_u()
print('u', srp.get_u())
srp.calculate_S_client()
print('S', srp.get_S())
srp.calculate_K()
print('K', srp.get_K())
srp.calculate_M1()
print('M1', srp.get_M1())
srp.calculate_M2()
