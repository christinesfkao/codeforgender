class Hash
  def to_utf8
    Hash[
      self.collect do |k, v|
        if (v.respond_to?(:to_utf8))
          [ k, v.to_utf8 ]
        elsif (v.respond_to?(:encoding))
          [ k, v.dup.force_encoding("ISO-8859-1").encode("UTF-8") ]
        else
          [ k, v ]
        end
      end
    ]
  end
end