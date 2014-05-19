set pagination off


 display /5i $eip

b *0x080493D7
commands
silent
p "alloca argument"
i r eax
c
end

b *0x80493E6
commands
silent
p "stack buffer location"
i r eax
c
end

b *0x08049403
commands
silent
p "stream after fopen"
i r eax
c
end


b *0x08049427
commands
silent
i r edx
c
end



b *0x8049253
commands
silent
p "cookie"
p /x $ebp-0xc
c
end


b *0x08049421
commands
silent
i r eax
c
end


b *0x0804952D
commands
silent
p "cookie/ret time"

end

b *0x08049544
commands
silent
p "ret"

end