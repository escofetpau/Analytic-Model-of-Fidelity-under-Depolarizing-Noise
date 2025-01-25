// Benchmark was created by MQT Bench on 2024-03-18
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 1.1.0
// Qiskit version: 1.0.2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[6];
creg meas[6];
u2(2.0,-pi) q[0];
u2(2.0,-pi) q[1];
cx q[0],q[1];
p(9.172838187819544) q[1];
cx q[0],q[1];
u2(2.0,-pi) q[2];
cx q[0],q[2];
p(9.172838187819544) q[2];
cx q[0],q[2];
cx q[1],q[2];
p(9.172838187819544) q[2];
cx q[1],q[2];
u2(2.0,-pi) q[3];
cx q[0],q[3];
p(9.172838187819544) q[3];
cx q[0],q[3];
cx q[1],q[3];
p(9.172838187819544) q[3];
cx q[1],q[3];
cx q[2],q[3];
p(9.172838187819544) q[3];
cx q[2],q[3];
u2(2.0,-pi) q[4];
cx q[0],q[4];
p(9.172838187819544) q[4];
cx q[0],q[4];
cx q[1],q[4];
p(9.172838187819544) q[4];
cx q[1],q[4];
cx q[2],q[4];
p(9.172838187819544) q[4];
cx q[2],q[4];
cx q[3],q[4];
p(9.172838187819544) q[4];
cx q[3],q[4];
u2(2.0,-pi) q[5];
cx q[0],q[5];
p(9.172838187819544) q[5];
cx q[0],q[5];
u2(2.0,-pi) q[0];
cx q[1],q[5];
p(9.172838187819544) q[5];
cx q[1],q[5];
u2(2.0,-pi) q[1];
cx q[0],q[1];
p(9.172838187819544) q[1];
cx q[0],q[1];
cx q[2],q[5];
p(9.172838187819544) q[5];
cx q[2],q[5];
u2(2.0,-pi) q[2];
cx q[0],q[2];
p(9.172838187819544) q[2];
cx q[0],q[2];
cx q[1],q[2];
p(9.172838187819544) q[2];
cx q[1],q[2];
cx q[3],q[5];
p(9.172838187819544) q[5];
cx q[3],q[5];
u2(2.0,-pi) q[3];
cx q[0],q[3];
p(9.172838187819544) q[3];
cx q[0],q[3];
cx q[1],q[3];
p(9.172838187819544) q[3];
cx q[1],q[3];
cx q[2],q[3];
p(9.172838187819544) q[3];
cx q[2],q[3];
cx q[4],q[5];
p(9.172838187819544) q[5];
cx q[4],q[5];
u2(2.0,-pi) q[4];
cx q[0],q[4];
p(9.172838187819544) q[4];
cx q[0],q[4];
cx q[1],q[4];
p(9.172838187819544) q[4];
cx q[1],q[4];
cx q[2],q[4];
p(9.172838187819544) q[4];
cx q[2],q[4];
cx q[3],q[4];
p(9.172838187819544) q[4];
cx q[3],q[4];
u2(2.0,-pi) q[5];
cx q[0],q[5];
p(9.172838187819544) q[5];
cx q[0],q[5];
ry(0.9081392660587984) q[0];
cx q[1],q[5];
p(9.172838187819544) q[5];
cx q[1],q[5];
ry(0.03002252160676866) q[1];
cx q[2],q[5];
p(9.172838187819544) q[5];
cx q[2],q[5];
ry(0.028972490260970152) q[2];
cx q[3],q[5];
p(9.172838187819544) q[5];
cx q[3],q[5];
ry(0.8605917057915445) q[3];
cx q[4],q[5];
p(9.172838187819544) q[5];
cx q[4],q[5];
ry(0.51293357944617) q[4];
ry(0.00260279915755246) q[5];
cx q[4],q[5];
cx q[3],q[4];
cx q[2],q[3];
cx q[1],q[2];
cx q[0],q[1];
ry(0.5448997311666637) q[0];
ry(0.44575498523091717) q[1];
ry(0.2601552932871516) q[2];
ry(0.06562035097558072) q[3];
ry(0.1442380099684526) q[4];
ry(0.5159476453907239) q[5];
barrier q[0],q[1],q[2],q[3],q[4],q[5];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
measure q[5] -> meas[5];