from fileinput import filename
import bs4

class OutputHTML:
    @staticmethod
    def generate_html(filename,total_no_of_banks,total_no_of_schools,total_no_of_pumps,peak_strings,non_peak_strings,population,pop_times_str):
        # load the file
        with open(filename) as inf:
            txt = inf.read()
            soup = bs4.BeautifulSoup(txt)

        soup.html.head.append(soup.new_tag("link", href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css",rel="stylesheet"))
        soup.html.head.title.extract()
        page_title = soup.new_tag("title")
        page_title.string="PSO - Location Intelligent System"
        soup.html.head.append(page_title)
        soup.html.body.extract()
        # create new link
        new_body = soup.new_tag("body", style="margin:0px; padding:0px; display: flex;",onload="initialize()")
        # insert it into the document
        soup.html.append(new_body)

        # bar chart

        add_bar_chart_link = soup.new_tag("script",src="https://cdn.jsdelivr.net/npm/chart.js")
        bar_chart = soup.new_tag("div", Class="shadow-lg rounded-lg overflow-hidden")
        inner_details = soup.new_tag("canvas",Class="p-10",id="chartBar")
        bar_chart.append(inner_details)

        # script
        bar_chart_data = soup.new_tag("script")
        bar_chart_data.string = """const labelsBarChart = ["12:00 AM","01:00 AM","02:00 AM","03:00 AM","04:00 AM","05:00 AM","06:00 AM","07:00 AM","08:00 AM","09:00 AM","10:00 AM","11:00 AM","12:00 PM","01:00 PM","02:00 PM","03:00 PM","04:00 PM","05:00 PM","06:00 PM","07:00 PM","08:00 PM","09:00 PM","10:00 PM","11:00 PM","11:59 PM"];
            const dataBarChart = {
            labels: labelsBarChart,
            datasets: [
                {
                label: "My First dataset",
                backgroundColor: "hsl(252, 82.9%, 67.8%)",
                borderColor: "hsl(252, 82.9%, 67.8%)",
                data: """ + pop_times_str +""",
                },
            ],
            };
        
            const configBarChart = {
            type: "bar",
            data: dataBarChart,
            options: {},
            };
        
            var chartBar = new Chart(
            document.getElementById("chartBar"),
            configBarChart
            );"""




        # add scripts for bar chart to body
        soup.html.body.append(add_bar_chart_link)
        soup.html.body.append(bar_chart_data)



        #end 

        soup.html.body.append(soup.new_tag("div",id="map_canvas", style="width: 50vw; height: 100vh"))
        summary_tag = soup.new_tag("div",style="width: 50vw; height: 100vh",Class="flex flex-col bg-gradient-to-r from-cyan-500 to-blue-500")
        #summary details
        img_tag = soup.new_tag("img",src="../src/logo.png", alt="Girl in a jacket" ,width="150", height="150")
        title_tag = soup.new_tag("h6",Class="m-4 font-bold font-italic text-2xl text-blue-800")
        title_tag.string = "Analysis Summary of Area (5KM)"
        dividend_tag = soup.new_tag("div",Class="divide-y-2 divide-black m-4 bg-yellow-500 rounded")
        schools = soup.new_tag("h6",Class="pl-2 text-green-800 ml-2")
        if total_no_of_schools == 60:
            schools.string="1. Schools/Universities: "+str(total_no_of_schools)+"+"
        else:
            schools.string="1. Schools/Universities: "+str(total_no_of_schools)
        banks = soup.new_tag("h6",Class="pl-2 text-green-800 ml-2")
        if total_no_of_banks == 60:
            banks.string="2. Banks/ATMS: "+str(total_no_of_banks)+"+"
        else:
            banks.string="2. Banks/ATMS: "+str(total_no_of_banks)
        pumps = soup.new_tag("h6",Class="pl-2 text-green-800 ml-2")
        if total_no_of_pumps == 60:
            pumps.string="3. Petrol Pumps: "+str(total_no_of_pumps)+"+"
        else:
            pumps.string="3. Petrol Pumps: "+str(total_no_of_pumps)

        peak_hours_yes = soup.new_tag("h6",Class="pl-2 text-blue-800 ml-2")
        peak_hours_no = soup.new_tag("h6",Class="pl-2 text-blue-800 ml-2")
        peak_hours_yes.string="4. Peak Hours: "
        peak_hours_no.string="5. Off-Peak Hours:"

        peaky_hours = soup.new_tag("h6",Class="ml-2")
        peaky_hours.string = peak_strings

        non_peaky_hours = soup.new_tag("h6",Class="ml-2")
        non_peaky_hours.string = non_peak_strings

        peak_hours_yes.append(peaky_hours)
        peak_hours_no.append(non_peaky_hours)

        area_type = soup.new_tag("h6",Class="pl-2 text-blue-800 ml-2")
        area_type_string = soup.new_tag("h6",Class="ml-2")



        if total_no_of_banks >= 30 and total_no_of_pumps >= 20 and total_no_of_schools >= 30:
            area_type.string="6. Area Type:"
            area_type_string.string = "Urban Area"
            area_type.append(area_type_string)
        else:
            area_type.string="6. Area Type:"
            area_type_string.string = "Rural Area"
            area_type.append(area_type_string)


        #population
        population_tag = soup.new_tag("h6",Class="pl-2 text-green-800 ml-2")
        population_tag.string = "7. Population Of City: "+str(population)



        # acknowledge_tag = "Project Supervised By: "
        # ack_tag = soup.new_tag("h1",Class="text-red-800 mt-5 ml-5 text-xl")
        # ack_tag.string = acknowledge_tag
        # first_name =  soup.new_tag("h6",Class="ml-4")
        # first_name.string = "Muhammad Nadeem Shamim"
        # second_name = soup.new_tag("h6",Class="ml-4")
        # second_name.string = "Mr.Abdullah Jawad" 
        # ack_tag.append(first_name)
        # ack_tag.append(second_name)



        dividend_tag.append(schools)
        dividend_tag.append(banks)
        dividend_tag.append(pumps)
        dividend_tag.append(peak_hours_yes)
        dividend_tag.append(peak_hours_no)
        dividend_tag.append(area_type)
        dividend_tag.append(population_tag)
        summary_tag.append(img_tag)
        summary_tag.append(title_tag)
        summary_tag.append(dividend_tag)
        summary_tag.append(bar_chart)
        summary_tag.append(bar_chart_data)
        # summary_tag.append(ack_tag)

        soup.html.body.append(summary_tag)


        # save the file again
        with open(filename, "w") as outf:
            outf.write(str(soup))
