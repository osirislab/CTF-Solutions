display /5i $eip

b *0x08048C62
commands
silent
p "execl"

end


b *0x8048FD2
commands
silent
p "cookie val"
i r eax
c
end

b *0x080490F0
commands
silent
p "check cookie"
i r eax

end

b *0x80490FF
commands
silent
p "return from mouse"

end
