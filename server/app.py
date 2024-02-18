V='localhost'
U='password'
T='user'
S='host'
R='config.json'
Q=Exception
N='message'
M='database'
I='success'
H=int
G=print
B='mysql'
D=True
C=str
from flask import Flask,request as W,jsonify as E
import json as O
from MySQLdb import connect as X
import paho.mqtt.client as P,python_artnet as l,os
from getmac import get_mac_address as Y
import time,sys
from multiprocessing import Process as J,Pipe
from ast import literal_eval as b
K=Flask(__name__)
Z=C(Y(interface='wlan0'))
try:
	with open(R,'r')as L:A=O.load(L)
except FileNotFoundError:
	A={B:{S:V,T:'pxm',U:'pixel',M:'pixeltube_db'}}
	with open(R,'w')as L:O.dump(A,L,indent=4)
o=A[B][M]
F=X(host=A[B][S],user=A[B][T],password=A[B][U],database=A[B][M])
F.autocommit(D)
p='PiXelTubeMaster-'+Z
def a(mac_address):
	B=mac_address;A=F.cursor();A.execute('SELECT * FROM tubes WHERE mac_address = %s',(B,));C=A.fetchone()
	if not C:A.execute('INSERT INTO tubes (mac_address, universe, dmx_address) VALUES (%s, %s, %s)',(B,0,1))
	else:0
	A.close()
@K.route('/register_tube',methods=['POST'])
def q():A=W.form.get('mac_address');a(C(A));return E({I:D,N:'Tube registered successfully.'})
@K.route('/get_assigned_params/<tube_unique_id>',methods=['GET'])
def r(tube_unique_id):
	C=False
	try:
		A=F.cursor();A.execute('SELECT universe, dmx_address FROM tubes WHERE mac_address = %s',(tube_unique_id,));B=A.fetchone();A.close()
		if B:G,H=B;return E({I:D,'universe':G,'dmx_address':H})
		else:return E({I:C,N:'Tube not found in the database'})
	except Q as J:return E({I:C,N:f"Error: {J}"})
def c():K.run(host='192.168.0.1',port=5000)
def m():
	try:A=C(os.system("ip -4 -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1 "));return A
	except(KeyError,IndexError,OSError)as B:G(f"Error getting eth0 IP: {B}");exit
def d(client,userdata,flags,reason_code,properties):
	A=reason_code
	if A==0:G('Connected to MQTT Broker!')
	else:G('Failed to connect, return code %d\n',C(A))
def n():A=P.Client(P.CallbackAPIVersion.VERSION2);A.on_connect=d;A.connect(V,1883);return A
def e(ti_receiver):
	k='/pixel_colors';j='tube-';i='PiXelTubeMaster';c=ti_receiver;G=None;d=n();o=m();e=l.Artnet(BINDIP=o,DEBUG=D,SHORTNAME=i,LONGNAME=i,PORT=6454)
	while D:
		try:
			F=e.readPacket()
			if c.poll():
				f=c.recv();g,h=b(f),b(f)
				if F is not G:
					A=F.data
					if g is not G:
						for E in g:
							if F.universe==H(E[1]):B=H(E[2]);I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z=A[B],A[B+1],A[B+2],A[B+3],A[B+4],A[B+5],A[B+6],A[B+7],A[B+8],A[B+9],A[B+10],A[B+11],A[B+12],A[B+13],A[B+14],A[B+15],A[B+16],A[B+17];a=j+C(E[0])+k;d.publish(a,C([C([K,I,J]),C([N,L,M]),C([Q,O,P]),C([T,R,S]),C([W,U,V]),C([Z,X,Y])]))
			elif F is not G:
				A=F.data
				if h is not G:
					for E in h:
						if F.universe==H(E[1]):B=H(E[2]);I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z=A[B],A[B+1],A[B+2],A[B+3],A[B+4],A[B+5],A[B+6],A[B+7],A[B+8],A[B+9],A[B+10],A[B+11],A[B+12],A[B+13],A[B+14],A[B+15],A[B+16],A[B+17];a=j+C(E[0])+k;d.publish(a,C([C([K,I,J]),C([N,L,M]),C([Q,O,P]),C([T,R,S]),C([W,U,V]),C([Z,X,Y])]))
		except KeyboardInterrupt:e.close();sys.exit()
def f(ti_sender):
	while D:
		try:A=F.cursor();A.execute('SELECT mac_address, universe, dmx_address FROM tubes');B=A.fetchall();A.close();ti_sender.send(C(B))
		except Q as E:G(E)
		time.sleep(2)
if __name__=='__main__':g,h=Pipe(D);i=J(target=f,args=(h,));i.start();j=J(target=e,args=(g,));j.start();k=J(target=c);k.start()