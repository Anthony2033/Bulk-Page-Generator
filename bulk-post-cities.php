<?php

// Define file locations
$wp_load_path = './wp-load.php';
$page_id = 1009; // ID of the WordPress page to use as a template
$csv_file_path = './cities.csv';

// Include WordPress core files
require_once($wp_load_path);

// Function to read CSV file
function read_csv($file_path) {
    $csv_data = array();
    if (($handle = fopen($file_path, "r")) !== FALSE) {
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            $csv_data[] = $data;
        }
        fclose($handle);
    }
    return $csv_data;
}

// Function to create WordPress pages
function create_wp_pages($pages) {
    foreach ($pages as $page) {
        $post = array(
            'post_title' => $page[0],
            'post_content' => $page[1],
            'post_type' => 'cities',
            'post_status' => 'publish',
        );
        wp_insert_post($post);
    }
}

// Function to generate WordPress pages with dynamic content from CSV file
function generate_pages($page_id, $csv_file_path) {
    // Get the HTML code of the WordPress page
    $page_content = get_post_field('post_content', $page_id);
    $html_code = $page_content;

    // Read the CSV file and generate the pages
    $csv_data = read_csv($csv_file_path);
    $header_row = array_shift($csv_data);
    foreach ($csv_data as $data) {
        $page_content = $html_code;
        foreach ($header_row as $index => $placeholder) {
            $value = $data[$index];
            $page_content = str_replace('['.$placeholder.']', $value, $page_content);
        }
        $pages[] = array($data[0], $page_content);
    }
    create_wp_pages($pages);
}

// Call the generate_pages function
generate_pages($page_id, $csv_file_path);

?>
