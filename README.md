# quicklink-cloud-functions
Google Cloud Function for getting url list of critical files for loading in Quicklink.js

Creates a cloud function in python which fetches the critical files of future navigations (example JS and CSS) into a list. 
This list can be passed as an arg to the quicklink.js library

Example:
You need every critical CSS and JS File of landing page , category page(PLP) and product page(PDP) in a list.
Why? Because you need to specify a list of urls which should be prefetched with the quicklink.js
(Of course you can use the elements) This is only for static urls.

Example of quicklink.js + cloud function: follows,
Live example of production environment: www.lights.ie
