# Bulk-Page-Generator
A script I made at my last job to upload bulk wordpress pages using CSV's as input
If you added a key.txt with a registered chatgpt API you could do some bulk generating yourself. 


# Overview of the Script
The bulk page generation script is a tool that automates the process of generating bulk pages for your WordPress website using content provided from a CSV file. It utilizes ChatGPT and Python scripting to create content for each page, allowing you to quickly populate your website with custom content. The script takes a wordpress page provided by its page ID and uses it as a template replacing placeholders in the template with the corresponding values from the CSV file and creating new pages with the generated content. Additionally this guide adds a custom post type of “cities” where your generated pages will live for organization and styling purposes.
Generating ChatGPT Content with Python Script
Before we begin generating pages we should first create ChatGPT content that we can include in our CSV so each page has a dash of custom content related to the city. To generate bulk content using ChatGPT, you'll need to open the ChatGPT.py file provided in your preferred IDE (I recommend VSCode). This script will interface with the ChatGPT API and allows you to provide an input CSV file and generates an output CSV file with responses from ChatGPT. To begin, make sure the API Key in the key.txt file is active and has billing set up. Visit https://platform.openai.com/account/api-keys under the admin@alexamediamarketing account to see if the API key is active.

Open the pythonGPT folder and modify the first row of the input.csv file to include the prompts you would like generated and save the file. I’ve included a promptFormating.csv file to give an example of how I typically create the prompts for each city. After your desired prompts are saved in input.txt, Select run > run  without debugging in VScode. If python has not been previously installed on your computer you may get an error. You can check if python is installed on your computer by running python --version in your VSCode terminal; visit this site to Install python for your OS if no version appears.

After installing python, validating the API Key, and modifying the input.csv file to your liking, Run the script in VSCode using run > run  without debugging. If there are any errors when executing the script ask Devon for help immediately and pray to baby Jesus. After praying you should start seeing outputs in the terminal indicating which prompts have been generated and if there are any errors.  Check the generated output.csv file to confirm the GPT content that was generated is to your liking and no UTF encoding errors occurred, you’re ready to add this content to your php script.
Setup your PHP script’s CSV File
Before running the script, You need to modify the cities.csv rows to include the content you want the placeholders in your wordpress template page to be filled with. Below is a visual example to elaborate on what I mean.


# Adding Custom Post Type to WordPress Site
Before running the script, we need to initialize a custom post type where the generated pages will live. In the left-hand menu in WP, Navigate to Apperance > Theme File Editor. Under theme files on the right-hand side select Theme Functions and paste the following code at the bottom file contents and press save:

 /*Custom Post type start*/
function cw_post_type_cities() {
$supports = array(
'title', // post title
'editor', // post content
'author', // post author
'thumbnail', // featured images
'excerpt', // post excerpt
'custom-fields', // custom fields
'comments', // post comments
'revisions', // post revisions
'post-formats', // post formats
'page-attributes', // templates
'post-templates', 
);
$labels = array(
'name' => _x('cities', 'plural'),
'singular_name' => _x('city', 'singular'),
'menu_name' => _x('cities', 'admin menu'),
'name_admin_bar' => _x('cities', 'admin bar'),
'add_new' => _x('Add New', 'add new'),
'add_new_item' => __('Add New city'),
'new_item' => __('New cities'),
'edit_item' => __('Edit city'),
'view_item' => __('View city'),
'all_items' => __('All cities'),
'search_items' => __('Search cities'),
'not_found' => __('No cities found.'),
);
$args = array(
'supports' => $supports,
'labels' => $labels,
'public' => true,
'query_var' => true,
'rewrite' => array('slug' => 'city'),
'has_archive' => true,
'hierarchical' => false,
);
register_post_type('cities', $args);
}
add_action('init', 'cw_post_type_cities');
/*Custom Post type end*/
  
# Styling your WP site
If this was done successfully, you should now see a “cities” post type in your left-hand WP sidebar. 
Setting up Your Styling and Generic Content with Theme Builder
To ensure consistent styling and design across the generated pages, you need to use theme builder to create a template for “city” post pages. Navigate to templates > Theme Builder > Single Post and click “Add New.”

Anywhere you want the city name displayed include a “Post Title” element. Include a Post Content element somewhere in the page to determine where the PHP Script content will be placed. Any other elementor elements and content will be included in all generated pages. Here’s a visual example using the Theme builder for Medicare Advantage Center as an example:  After you finish creating your template page and press “publish” add the condition  “cities.”    Creating the template page for the Post Content
Once your generic Theme Builder page is created, it's time to create a wordpress page that determines how your dynamic spreadsheet content will be displayed. This page should be created without elementor. Create a new Wordpress Page; Anywhere you want the data from your CSV file to be placed, write the column header in brackets. Here is an example of a created WP template page for Medicare with a CSV file with the headers “city”, “state_name”, and “county_name”. 



You can put your ChatGPT content in a CSV column heading titled “content1” and include [content1] on this template page wherever you want your ChatGPT content to go.   Once your finished making your Bulk content Template copy the page ID in the site URL; This page ID will be set in the PHP script so the program knows what pages to grab content from to be replaced. 

EX: https://medhealth-advisors.com/wp-admin/post.php?post=2894&action=elementor. 

Open the bulk-post-cities.php file with a text editor of your choice and modify the $page_id = 1009; to your previously copied page ID. While you’re here also change the $csv_file_path = './cities.csv'; to the CSV filename of your choice, or keep it untouched and make sure your CSV file is named “cities”. 
Connecting to the WP Server and Running the Script
Once your WordPress site, template pages, and CSV file is set up, it's finally time to connect to the WP server to add and run the script (This is the fun hacker part where all your work pays off). You first need to download a SSH client to connect to the wordpress server (I recommend Filezilla.) 

Go to access details of your chosen site in cloudways and create APPLICATION CREDENTIALS by adding a Username and Password for your site. In filezilla enter in the credentials you just created along with the IP address in “Host:” and 22 in “Port” and press quickconnect. Navigate into public_html > and copy the cities CSV file and PHP File to the server. In cloudways open a new tab under “view server details” and click “Launch SSH Terminal.” and paste your login credentials (Right-click > paste from Browser).   Once logged in type “cd applications” and press enter. Then type ls to see a list of the wordpress servers and navigate into your server by typing “cd (server name)” You can find the server name of your site on the access details page in cloudways: 

Type “cd public_html/” and press enter. When you now type ls you should see “bulk-post-cities.php” in the listed files. If the file is there type “php bulk-post-cities” and press enter to run the script and wait for the terminal to return a new line. When checking your wordpress cities tab you should see as many pages generated as there were columns of data in your cities.csv file.   If when you view a city page and it says “page not found” navigate to your wordpress settings and under permalinks (forgot what to do). 

# Extra Info    
Most of the Csvs provided in the Useful Resources folder can be found in the Google Drive and is personally my preferred way to format data and URL’s.                             The Bulk Page Generator was created by Anthony Colangelo and wouldn’t be possible without the close collaboration and guidance from Devon!
