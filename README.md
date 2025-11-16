# QR Code Generator with Image Overlay

This project is a web-based QR code generator built with FastAPI that allows you to create QR codes with custom logos or overlay them onto images.

## Description

This application provides a simple and intuitive web interface to generate QR codes. You can either embed a logo in the center of a QR code or overlay a QR code onto a larger image. The application is built with Python and the FastAPI framework, with a simple HTML, CSS, and JavaScript frontend.

## Features

-   **Two Modes:**
    -   **Logo Mode:** Embed a custom logo into the center of a QR code.
    -   **Overlay Mode:** Overlay a QR code onto an existing image.
-   **Customizable QR Code:**
    -   Set the URL to be encoded.
    -   Choose the position of the QR code overlay (top-left, top-right, bottom-left, bottom-right).
    -   Adjust the size of the QR code relative to the image.
    -   Set the margin around the QR code.
-   **Web Interface:**
    -   A simple and user-friendly web interface to generate QR codes without any coding.
    -   Real-time preview of the generated QR code.
    -   Download the generated QR code as a PNG or JPEG image.

## Getting Started

### Prerequisites

-   Python 3.7+
-   pip

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/banksythequantLab/qr-generator.git
    cd qr-generator
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application:**

    ```bash
    uvicorn main:app --reload --port 7899
    ```

2.  **Open your browser:**

    Navigate to `http://127.0.0.1:7899` in your web browser.

3.  **Use the web interface:**
    -   Fill out the form with your desired URL, image, and other settings.
    -   Click "Generate QR Code".
    -   The generated QR code will be displayed on the right side of the page.
    -   Click the "Download Image" button to save the generated QR code.

## API Endpoint

The application provides a single API endpoint to generate QR codes programmatically.

### `POST /qr-with-image`

This endpoint accepts a `multipart/form-data` request with the following fields:

-   `image`: The image file to be used as a logo or background.
-   `url`: The URL to be encoded in the QR code.
-   `mode`: The mode of operation. Can be `logo` or `overlay`. Defaults to `overlay`.
-   `position`: The position of the QR code in overlay mode. Can be `top_left`, `top_right`, `bottom_left`, or `bottom_right`. Defaults to `bottom_right`.
-   `qr_size`: The size of the QR code as a fraction of the image width. Defaults to `0.2`.
-   `margin`: The margin around the QR code in pixels. Defaults to `32`.
-   `output_format`: The output format of the generated image. Can be `png` or `jpeg`. Defaults to `png`.

The endpoint returns the generated QR code image as a response with the appropriate `Content-Type` header.