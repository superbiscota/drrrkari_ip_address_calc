#   Copyright [ron]
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import hashlib

name      =  "ron"
target_id =  "5befaa85b5176954561d90ab40df4718"

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
	D =  (index % 256)
	C =  ((index >> 8) & 0b11111111 )
	B =  ((index >>16) & 0b11111111 )
	A =  (index >> 24) 
	return "{a}.{b}.{c}.{d}".format (a = A ,b = B ,c = C ,d = D)

#ip_generator(589824)
for itr in range(4294967295) :
	# 4294967 = 0.1% 
	wait = 0#1005000000
	ip_adress  = ip_generator(itr + wait)
	if (itr % 4294967 == 0 and itr > 0) :
		print (str (itr/4294967295  * 100) + "% " + ip_adress)
	
	ret = check(target_id,ip_adress)
	if (ret == 1) : 
		break



