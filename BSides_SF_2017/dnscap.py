import pyshark, struct
cap = pyshark.FileCapture('/Users/nickgregory/Downloads/dnscap.pcap')

def ans(pkt):
    resp = None
    if pkt.resp_type == '15':
        resp = pkt.mx_mail_exchange.split('.skullseclabs')[0]
    elif pkt.resp_type == '16':
        resp = pkt.txt
    elif pkt.resp_type == '5':
        resp = pkt.cname.split('.skullseclabs')[0]
    else:
        print "Unhandled response type:", pkt.resp_type
        return resp
    
    resp = resp.replace('.', '')
    return resp


def decode_header(data):
    pkt_id, pkt_type, sess_id = struct.unpack('>HBH', data[:5])
    if pkt_type == 0: #PACKET_TYPE_SYN
        seq_id, options = struct.unpack('>HH', data[5:9])
        print "SYN pkt with id {} in session {} has seq {} and options {}".format(pkt_id, sess_id, seq_id, options)
    elif pkt_type == 1: #PACKET_TYPE_MSG
        seq_id, ack_id = struct.unpack('>HH', data[5:9])
        print "MSG pkt with id {} in session {} has seq {}, acks {}".format(pkt_id, sess_id, seq_id, ack_id)
    else:
        seq_id = None
        print "Pkt id {} is of unknown type {}".format(pkt_id, pkt_type)
    
    return seq_id

result = ""
last_seq = 0

for pkt in cap:
    if int(pkt.number) > 50 and int(pkt.number) < 341:
        if hasattr(pkt.dns, 'resp_type'):
            q_id = int(pkt.dns.response_to) - 1
            q = cap[q_id].dns.qry_name.split('.skullseclabs')[0].replace('.', '').decode('hex')
            if last_seq < decode_header(q):
                last_seq = decode_header(q)
                result += q[9:]
        
                print "Query ({}):".format(q_id + 1), repr(cap[q_id].dns.qry_name.split('.skullseclabs')[0].replace('.', '').decode('hex'))
                print "Response ({}):".format(pkt.number), repr(ans(pkt.dns).decode('hex'))
            else:
                print "Skipping pkt {} due to OOO".format(q_id+1)
    else:
        if hasattr(pkt.dns, 'resp_type'):
            print "Response ({}):".format(pkt.number), repr(ans(pkt.dns).decode('hex'))
        else:
            print "Query ({}):".format(pkt.number), repr(pkt.dns.qry_name.split('.skullseclabs')[0].replace('.', '').decode('hex'))
        

file_len, pkt_id, cmd_id = struct.unpack('>IHH', result[:8])
print "Got command data: len {}, pkt_id {}, cmd_id {}".format(file_len, pkt_id, cmd_id)
result = result[8:]

f = open('out.png', 'wb')
f.write(result)
f.close()