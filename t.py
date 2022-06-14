import joblib
import hashlib
import time

name          =  "ron"
target_id     =  "5befaa85b5176954561d90ab40df4718"

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

start_time = time.time()

def sweeper(itr) :
	#for itr in range(from_num , to_num) :
	deci_percent = int (  ( MAX_IP_ADRESS_RANGE ) / 1000 ) 
	ip_adress  = ip_generator(itr + SKIP_IP_ADRESS_ZONE )
	if (itr % deci_percent == 0 and itr > 0) : # 0.1% = deci %		
		now_time = time.time()
		past_time = now_time - start_time # 秒
		 # revolution per sec
		print ( "process " +  str (int(itr/( MAX_IP_ADRESS_RANGE ) * 10000)/100) + "%   " + str (int (itr / past_time) ) + " r/sec "  + " 《" + ip_adress + "》 ")
	ret = check(target_id,ip_adress)

#tpe = ThreadPoolExecutor(max_workers=MAX_WORKER)

joblib.Parallel(n_jobs=-1)(joblib.delayed(sweeper)(i) for i in range( 1       , int  (MAX_IP_ADRESS_RANGE )))