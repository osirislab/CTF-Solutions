load 't.rb'
require 'fileutils'

s = 1447200000
e = 1447372800

for i in s..e
    begin
        r = RandSomewhere.new('Rm9yIHRoaW5ncyB0byByZXZlYWwgdGhlbXNlbHZlcyB0byB1cywgd2UgbmVlZCB0byBiZSByZWFkeSB0byBhYmFuZG9uIG91ciB2aWV3cyBhYm91dCB0aGVtLg==', 'fakehiddenservicenotpartofthechallenge', '006AFF07', i)
        r.decrypt_file('flag.png.encrypted')
        FileUtils.mv('flag.png.encrypted.decrypted', "o/#{i}.png")
        puts(i)
    rescue
        next
    end
end
