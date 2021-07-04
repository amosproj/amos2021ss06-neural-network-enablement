// helpers

function showWarningToast(headline, message) {
  let node = document.createElement('div');
  node.innerHTML = document.querySelector('#template-toast-warn').innerHTML;

  node.querySelector('#toast-headline').textContent = headline;
  node.querySelector('#toast-message').textContent = message;

  Toastify({
    node: node,
    duration: 5000,
    close: true,
    gravity: "top", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    stopOnFocus: true, // Prevents dismissing of toast on hover
    backgroundColor: '#FDE68A', // bg-yellow-200 TODO: use style attribute
  }).showToast();
}


// -------------------------------------------------------------------------

// dropzone initialization stuff

let config = {
  url: "/media/",
  disablePreviews: true,
  //  acceptedFiles: ".jpeg,.jpg,.png,.gif,.mp4,.mkv,.webm"
};

let myDropzone1 = new Dropzone("#upload-button", config);
let myDropzone2 = new Dropzone("#upload-button-img", config);
let myDropzone3 = new Dropzone("#upload-button-text", config);

myDropzone1.on("success", successHandler);
myDropzone2.on("success", successHandler);
myDropzone3.on("success", successHandler);

myDropzone1.on("error", errorHandler);
myDropzone2.on("error", errorHandler);
myDropzone3.on("error", errorHandler);

// success handler: called, after dropzone library successfully uploaded a file
function successHandler(file, resp) {
  console.log('success!')
  //console.log(file)
  //console.log(resp)

  window.location.reload(true);
}


// error handler: called, after dropzone library fails to upload a file
function errorHandler(file, error, xhr) {
  console.log('error!')

  let message = 'Please try again.'

  if (typeof(error) === 'string') {

    if (error === 'Server responded with 0 code.') {
      // Improve default error message by dropzone
      message = "Couldn't connect to server. Is the service running?"
    } else {
      message = error;
    }

  } else {
    // print response by api
    message = error['msg']

  }

  showWarningToast('File upload failed', message);
}

// end dropzone stuff
// ---------------------------------------------------------------------------------------


// sends the service a request to delete the image
// after the user clicked on the 'delete icon'
function deleteImage(id) {
  console.log('deleteImage ' + id);

  $.ajax({
    type: "DELETE",
    url: "/media/" + encodeURI(id),
    success: function() {
      console.log('success');

      function reload() {
        window.location.reload(true);
      }

      setTimeout(reload, 500);
    },
    error: function() {
      showWarningToast("Deleting image failed.", "Couldn't connect to server. Is the service running?");
    },
    dataType: 'json',
    contentType: 'application/json',
  });
}


// sends the service a request to colorize the image
// after the user clicked on the 'colorize icon',
// if successful it calls the showResult function
function colorizeImageAndShowResult(id) {
  console.log(id, 'colorize')

  // call colorize function
  $.ajax({
    type: "POST",
    url: "/media/" + encodeURI(id) + "/colorize",
    success: function(response) {
      console.log(response['msg']);
      showResult(id);
    },
    error: function(error) {
      if (error.status === 500 || error.status === 400) {
        let msg = error['responseJSON']['msg'];
        showWarningToast("Colorizing image failed.", msg);
        console.log(msg);
      } else if (error.status === 0) {
        showWarningToast("Colorizing image failed.", "Couldn't connect to server. Is the service running?");
        console.log("Colorizing image failed.", error);
      } else {
        showWarningToast("Colorizing image failed.", "The error was logged to the" +
          " console.");
        console.log('Colorizing image failed.', error);
      }
    },
    dataType: 'json',
    contentType: 'application/json',
  });
}


// displays the original and the colorized image next to each other
function showResult(id) {
  console.log('showResult', id);

  $.ajax({
    type: "GET",
    url: "/media/" + encodeURI(id),
    success: function(response) {

      let type = response['type']
      let urlOriginal = response['origin']
      let urlColor = response['colorized']

      let original = null
      let colorized = null

      // show result page popup

      if (type === 'image') {

        // create images to add to result page
        original = $('<img />', {
          id: 'result-image-original',
          class: 'm-6 mr-4 py-6 text-center my-auto h-full w-full float-left object-contain',
          src: urlOriginal
        })

        colorized = $('<img />', {
          id: 'result-image-colorized',
          class: 'm-6 mr-4 py-6 text-center my-auto h-full w-full float-left object-contain',
          src: urlColor
        })

      } else {

        // create videos to add to result page
        original = $('<video controls autoplay muted />', {
          id: 'result-video-original',
          class: 'm-6 mr-4 py-6 text-center my-auto h-full w-full float-left object-contain',
          src: urlOriginal
        })

        colorized = $('<video controls autoplay muted />', {
          id: 'result-video-colorized',
          class: 'm-6 mr-4 py-6 text-center my-auto h-full w-full float-left object-contain',
          src: urlColor
        })
      }

      // clear old images / videos
      $('#result-div-original').empty()
      $('#result-div-colorized').empty()

      // add images / videos
      $('#result-div-original').append(original)
      $('#result-div-colorized').append(colorized)

      setTimeout(function() {
        document.querySelector('#result-colorize').classList.remove('invisible');
      }, 100);
    },
    error: function(error) {
      console.log(error);
      showWarningToast("Loading the result failed.", "Couldn't connect to server. Is the service running?");
    },
    dataType: 'json',
    contentType: 'application/json',
  });
}


// ---------------------------------------------------------------------------------------
// This is called on every page load.
//
// load images and display them in gallery
$.get('/media/', null, function(data) {
  if (data.length > 0) {
    document.getElementById('drpzn').classList.remove('invisible');

    data.sort(function(a, b) {
      return a.thumbnail.localeCompare(b.thumbnail);
    });

    data.forEach(function(data) {
      let id = data.id
      let type = data.type
      let thumbnail = data.thumbnail

      let div = document.createElement('div');
      div.innerHTML = document.querySelector('#template-gallery-image').innerHTML
      console.log(div)

      div.querySelector('#gallery-image').setAttribute('src', thumbnail);

      if (type === 'video') {
        div.querySelector('#video-icon').classList.remove('invisible');
      }

      let imgButton = div.querySelector('#delete-image-button');

      imgButton.onclick = function() {
        // only allow one mouseclick, remove the eventlistener after first click
        imgButton.onclick = function() {}

        deleteImage(id);
      }

      let colorizeButton = div.querySelector('#colorize-image-button');
      colorizeButton.onclick = function() {
        colorizeImageAndShowResult(id);
      }

      document.getElementById("drpzn").appendChild(div)
    })
  }
});
