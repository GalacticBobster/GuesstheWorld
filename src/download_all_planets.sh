#!/bin/bash

# Download planetary data for multi-planet geoguesser
# Creates data directory and downloads map images and nomenclature data

cd "$(dirname "$0")/.."
mkdir -p data
cd data

echo "Downloading planetary data..."

# Mars data (already in original script)
echo "Downloading Mars data..."
wget -nc https://asc-planetarynames-data.s3.us-west-2.amazonaws.com/MARS_nomenclature_center_pts.kmz
wget -nc https://astrogeology.usgs.gov/ckan/dataset/dfdc2242-52dc-4126-bc89-03af8253ae79/resource/0d7b31dc-0b2e-4ca6-89dc-e3c1404c0232/download/mars_viking_clrmosaic_global_1024.jpg

# Moon data
echo "Downloading Moon data..."
wget -nc https://asc-planetarynames-data.s3.us-west-2.amazonaws.com/MOON_nomenclature_center_pts.kmz
wget -nc https://astrogeology.usgs.gov/ckan/dataset/a8a35dbf-c4bb-4608-bb83-8073a2a9b0f8/resource/d6eb89c8-99ba-4ceb-a6d7-e0e7f1dd6c11/download/moon_lro_clrshade_global_1024.jpg -O moon_lro_clrshade_global_1024.jpg

# Venus data
echo "Downloading Venus data..."
wget -nc https://asc-planetarynames-data.s3.us-west-2.amazonaws.com/VENUS_nomenclature_center_pts.kmz
wget -nc https://astrogeology.usgs.gov/ckan/dataset/c4c3acbd-34db-4a75-85d3-08e03a6a1821/resource/f8cf35ff-f35c-496a-9dcf-8e10c3c1c3d3/download/venus_magellan_global_1024.jpg -O venus_magellan_global_1024.jpg

# Mercury data
echo "Downloading Mercury data..."
wget -nc https://asc-planetarynames-data.s3.us-west-2.amazonaws.com/MERCURY_nomenclature_center_pts.kmz
wget -nc https://astrogeology.usgs.gov/ckan/dataset/2d77c6d7-26fa-4e23-8b77-d3cf0f0e9e50/resource/8f3d19dc-04ff-4f31-8fdf-e8b5a55d2ec2/download/mercury_messenger_global_1024.jpg -O mercury_messenger_global_1024.jpg

echo "Download complete!"
echo "All planetary data has been downloaded to the data directory."
