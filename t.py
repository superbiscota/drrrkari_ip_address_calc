#from concurrent.futures import ThreadPoolExecutor
import threading
import hashlib
import time

name          =  "ron"
target_id     =  "5befaa85b5176954561d90ab40df4718"
MAX_WORKER    = 4


MAX_IP_ADRESS_RANGE  =  4278190079 + 1 # 4 thred で割り切れるようにするための + 1
SKIP_IP_ADRESS_ZONE  =  16777216

def check(target_id,ip_adress):
	drr_dat  = name + ip_adress
	if   ( hashlib.md5( drr_dat.encode() ).hexdigest() == target_id ) :
		print (" yep !!  {target_id}  is  {ip_adress}".format(target_id=target_id, ip_adress = ip_adress))
		return 1
	return 0

def ip_generator(index):
# make IP adress by index
#   AAA.BBB.CCC.DDD 
#   16777216 : 1.0.0.0
#   4294967295 : 255.255.255.255

##  16777216 to  4294967295
##        0   to  4278190079
	D =  (index % 256)
	C =  ((index >> 8) & 0b11111111 )
	B =  ((index >>16) & 0b11111111 )
	A =  (index >> 24) 
	return "{a}.{b}.{c}.{d}".format (a = A ,b = B ,c = C ,d = D)


def sweeper(label,from_num , to_num) :
	start_time = time.time()
	for itr in range(from_num , to_num) :
		deci_percent = int (  ( to_num - from_num ) / 1000 ) 
		ip_adress  = ip_generator(itr + SKIP_IP_ADRESS_ZONE )
		if (itr % deci_percent == 0 and itr > 0) : # 0.1% = deci %		
			now_time = time.time()
			past_time = now_time - start_time # 秒
		 # revolution per sec
			print ( "process " + label +  "  " + str (int(itr/( to_num - from_num )  * 10000)/100) + "%   " + str (int (itr / past_time) ) + " r/sec "  + " 《" + ip_adress + "》 ")
		ret = check(target_id,ip_adress)
		if (ret == 1) : 
			break




#tpe = ThreadPoolExecutor(max_workers=MAX_WORKER)

thread1 = threading.Thread(target=sweeper("A",                          1       , int  (MAX_IP_ADRESS_RANGE/4 * 1) ))
thread2 = threading.Thread(target=sweeper("B", int (MAX_IP_ADRESS_RANGE/4*1) +1 , int  (MAX_IP_ADRESS_RANGE/4 * 2) ))
thread3 = threading.Thread(target=sweeper("C", int (MAX_IP_ADRESS_RANGE/4*2) +1 , int  (MAX_IP_ADRESS_RANGE/4 * 3) ))
thread4 = threading.Thread(target=sweeper("D", int (MAX_IP_ADRESS_RANGE/4*3) +1 , int  (MAX_IP_ADRESS_RANGE/4 * 4) ))

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()