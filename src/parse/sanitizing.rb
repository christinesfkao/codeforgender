require 'nokogiri'
require 'pry'
require './parser.rb'
require './hash_extend.rb'

puts "想要 parse 哪個檔案～"
file_path = STDIN.gets.chomp

# [*2005..2016].each do |year|
# 	# Parser.new(year).parse_file('data/2015/M.1421905597.A.AD3.html')
# 	Parser.new(year).parse_folder
# end
# binding.prydata/2006/M.1136548860.A.6C9.html
Parser.new.parse_file("#{file_path}")