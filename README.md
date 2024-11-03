# pacs-implementation
Repository used to store implementation of the data storage solution

# PACS Configuration with Orthanc

This documentation provides a step-by-step guide on installing and configuring Orthanc as a PACS (Picture Archiving and Communication System) server on Ubuntu.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Service Commands](#service-commands)
- [Accessing Orthanc](#accessing-orthanc)
- [Reference](#reference)

---

## Overview

Orthanc is an open-source, lightweight, and RESTful DICOM server for healthcare and medical research. It provides a robust solution for handling, storing, and managing medical images and integrating with other systems using DICOM and REST APIs.

## Installation

To install Orthanc and its various plugins, run the following commands in your terminal:

```bash
# Install the base Orthanc package
sudo apt install orthanc

# Install additional Orthanc plugins
sudo apt install orthanc-dicomweb       # DICOMweb support
sudo apt install orthanc-gdcm           # Support for DICOM compression
sudo apt install orthanc-imagej         # Integration with ImageJ
sudo apt install orthanc-mysql          # MySQL storage plugin
sudo apt install orthanc-postgresql     # PostgreSQL storage plugin
sudo apt install orthanc-python         # Python scripting support
sudo apt install orthanc-webviewer      # Web viewer for DICOM images
sudo apt install orthanc-wsi            # Whole Slide Imaging (WSI) support
```


## Service Commands
----------------

To manage the Orthanc service, use the following commands:

bash

Copy code

`# Start the Orthanc service
sudo service orthanc start

# Stop the Orthanc service
sudo service orthanc stop

# Restart the Orthanc service
sudo service orthanc restart`

These commands allow you to start, stop, or restart the Orthanc service as needed.



## Accessing Orthanc
-----------------

Once Orthanc is installed and the service is running, you can access the Orthanc web interface using the following URL:

-   **URL**: <http://172.29.98.120:8042/>

 `172.29.98.120` . This URL opens the Orthanc web dashboard, allowing you to view, upload, and manage DICOM images through a web browser.


## Reference
---------

For more information on Orthanc installation and configuration, refer to the official documentation: [Orthanc Debian Packages](https://orthanc.uclouvain.be/book/users/debian-packages.html)
