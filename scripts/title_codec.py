"""Verified bank-2 decoder format: repeat, literal, increment, address change, end."""
def unpack(stream):
    address=int.from_bytes(stream[:2],'little');p=2;result={}
    while True:
        assert p<len(stream),'Unterminated title stream'
        c=stream[p];p+=1
        if c==0xFF:return result,p
        if c==0x7F:
            assert p+2<=len(stream);address=int.from_bytes(stream[p:p+2],'little');p+=2;continue
        if c>=0xC0:
            count=c&0x3F or 256
            values=bytes((stream[p]+i)&255 for i in range(count));p+=1
        elif c>=0x80:
            count=c&0x7F or 256;values=stream[p:p+count];p+=count;assert len(values)==count
        else:
            count=c or 256;values=bytes([stream[p]])*count;p+=1
        for v in values:
            assert 0x2000<=address<0x3000
            assert address not in result,'Overlapping title stream destination'
            result[address]=v;address+=1
def pack(data,address):
    # Cost-minimal canonical encoder. Reserved 7F/FF never used as count commands.
    n=len(data);cost=[0]*(n+1);choice=[None]*n
    for i in range(n-1,-1,-1):
        options=[(1+k+cost[i+k],'literal',k) for k in range(1,min(63,n-i)+1)]
        run=1
        while run<min(256,n-i) and data[i+run]==data[i]:run+=1
        options.extend((2+cost[i+k],'repeat',k) for k in range(1,min(126,run)+1))
        if run>=256:options.append((2+cost[i+256],'repeat',256))
        inc=1
        while inc<min(62,n-i) and data[i+inc]==(data[i]+inc)&255:inc+=1
        options.extend((2+cost[i+k],'increment',k) for k in range(1,inc+1))
        cost[i],kind,k=min(options);choice[i]=(kind,k)
    out=bytearray(address.to_bytes(2,'little'));i=0
    while i<n:
        kind,k=choice[i]
        if kind=='literal':out.append(0x80|k);out.extend(data[i:i+k])
        elif kind=='increment':out.extend((0xC0|k,data[i]))
        else:out.extend((k if k!=256 else 0,data[i]))
        i+=k
    out.append(255)
    decoded,_=unpack(out);assert bytes(decoded[a] for a in range(address,address+n))==data
    return bytes(out)
