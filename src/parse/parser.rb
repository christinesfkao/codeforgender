require 'json'

class Parser
	def initialize
		# @year = year
	end

	def parse_folder
		entries = Dir["data/#{@year}/*.html"]
		docs = Hash.new

		entries.each do |entry|
			self.parse_file(entry)
		end
	end

	def parse_file(entry)
		doc = Nokogiri::HTML(File.open(entry)) { |f| f.noblanks }

		sanitized_hash = Hash.new

		headers = doc.css("span.article-meta-value")
		body = doc.css("#main-content")

		sanitized_hash = { "file_name" => entry,
			"author" => headers[0].content.gsub('作者', ''),
			"board" => headers[1].content.gsub('看板', ''),
			"title" => headers[2].content.gsub('標題', ''),
			"time" => headers[3].content.gsub('時間', ''),
			"body" => body[0].xpath('text()').map { |c| c.content }.join,
			"push" => []
		}

		connected_push = []

		pushes = doc.css("div.push")
		pushes.each_with_index do |p, i|
			if i == 0
				a = { "push_type" => pushes[1].children[0].children[0].content,
					"author" => pushes[1].children[1].children[0].content,
					"content" => pushes[1].children[2].children[0].content
				}

				connected_push << a
			else
				a = { "push_type" => pushes[i].children[0].children[0].content,
					"author" => pushes[i].children[1].children[0].content,
					"content" => pushes[i].children[2].children[0].content
				}

				if connected_push[0]["author"] != pushes[i].children[1].children[0].content
					joined_content = connected_push.map { |c| c["content"] }.join
					connected_push[0]["content"] = joined_content
					sanitized_hash["push"] << connected_push[0]
					connected_push = []
					connected_push << a
				else
					connected_push << a
				end
			end
		end

	self.output_file(entry, sanitized_hash)

	rescue NoMethodError
		parse_file_ver_2(entry)
	end

	def parse_file_ver_2(entry)
		doc = Nokogiri::HTML(File.open(entry)) { |f| f.noblanks }

		sanitized_hash = Hash.new

		headers = doc.css("#main-content").children
		body = doc.css("#main-content")


		sanitized_hash = { "file_name" => entry,
			"author" => headers[0].content.gsub('作者', ''),
			"board" => headers[1].content.gsub('看板', ''),
			"title" => headers[2].content.gsub('標題', ''),
			"time" => headers[3].content.gsub('時間', ''),
			"body" => body[0].xpath('text()').to_a.join.gsub(/\n/, ""),
			"push" => []
		}

		pushes = doc.css("div.push:not(.warning-box)")

		connected_push = []

		pushes.each_with_index do |p, i|
			if pushes[i].children[0].children[0].nil? || pushes[i].children[1].children[0].nil? || pushes[i].children[2].children[0].nil?
				File.open("output_json/errors.json", "a") do |f|
					f.write(pushes[i].to_json)
				end
				next
			end

			if i == 0
				a = { "push_type" => pushes[1].children[0].children[0].content,
					"author" => pushes[1].children[1].children[0].content,
					"content" => pushes[1].children[2].children[0].content
				}

				connected_push << a
			else
				a = { "push_type" => pushes[i].children[0].children[0].content,
					"author" => pushes[i].children[1].children[0].content,
					"content" => pushes[i].children[2].children[0].content
				}

				if connected_push[0]["author"] != pushes[i].children[1].children[0].content
					joined_content = connected_push.map { |c| c["content"] }.join
					connected_push[0]["content"] = joined_content
					sanitized_hash["push"] << connected_push[0]
					connected_push = []
					connected_push << a
				else
					connected_push << a
				end
			end
		end

	self.output_file(entry, sanitized_hash)

	rescue NoMethodError => e
		if doc.css(".bbs-footer-message")[0].respond_to?(:content)
			output = "#{entry.split("/").last.gsub('.', '')} - #{doc.css(".bbs-footer-message")[0].content}"
		else
			output = entry
		end

		File.open("output_json/errors.json", "a") do |f|
			f.write(output)
		end
	end

	def output_file(entry, sanitized_hash)
		begin
			File.open("output_json/#{entry.split("/").last}.json", "w") do |f|
				f.write(sanitized_hash.to_json)
			end
		rescue => e
			File.open("output_json/errors.json", "a") do |f|
				f.write("#{entry} - #{e}")
			end
		end
	end
end