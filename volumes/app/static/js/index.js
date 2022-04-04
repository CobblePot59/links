  $(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();

    $("#data").DataTable({
      columns: [
        {orderable: false, searchable: true, "width": "50%"},
        {orderable: true, searchable: true, "width": "10%"},
        {orderable: false, searchable: true, "width": "15%"},
        {orderable: false, searchable: true, "width": "15%"},
        {orderable: false, searchable: false, "width": "10%"},
        ],
    });
  });

  $('#edit').on('show.bs.modal', function(e) {
    var linkId = $(e.relatedTarget).data('link-id');
    var linkUrl = $(e.relatedTarget).data('link-url');
    document.getElementById("eform").setAttribute("action", "/edit/"+linkId);
    document.getElementById("eurl").setAttribute("href", linkUrl);
    document.getElementById("eurl").innerText=linkUrl;
  });

  $('#delete').on('show.bs.modal', function(e) {
    var linkId = $(e.relatedTarget).data('link-id');
    var linkUrl = $(e.relatedTarget).data('link-url');
    document.getElementById("dform").setAttribute("action", "/delete/"+linkId);
    document.getElementById("durl").setAttribute("href", linkUrl);
    document.getElementById("durl").innerText=linkUrl;
  });

  function like(likeObject){
    let id = likeObject.id.split('-')[1];
    $.get('/like/'+id, (data) => {
      likeObject.lastChild.data = data.nb;
      $("#like-"+id).attr("data-bs-original-title", data.users);
    }, 'json');
  }

  function dislike(dislikeObject){
    let id = dislikeObject.id.split('-')[1];
    $.get('/dislike/'+id, (data) => {
      dislikeObject.lastChild.data = data.nb;
      $("#dislike-"+id).attr("data-bs-original-title", data.users);
    }, 'json');
  }


  function archive(archiveObject){
    let id = archiveObject.id.split('-')[1];
    $.get('/archive/'+ id, (data, status) => {
      if( status === "success"){
        if(data.archive != null && data.archive){
          document.getElementById("row-"+id).cells[0].children[0].style = "color:grey; text-decoration:line-through; pointer-events:none;"
          document.getElementById("row-"+id).cells[4].children[0].style = "pointer-events:none;"
          document.getElementById("row-"+id).cells[4].children[0].children[0].style = "color:grey;"
          document.getElementById("row-"+id).cells[4].children[1].style = "pointer-events:none;"
          document.getElementById("row-"+id).cells[4].children[1].children[0].style = "color:grey;"
          document.getElementById("row-"+id).cells[4].children[2].style = "color:grey; pointer-events:none;"
        }
        else if(data.restore != null && data.restore){
          document.getElementById("row-"+id).cells[0].children[0].style = ""
          document.getElementById("row-"+id).cells[4].children[0].style = ""
          document.getElementById("row-"+id).cells[4].children[0].children[0].style = "color:green; cursor:pointer;"
          document.getElementById("row-"+id).cells[4].children[1].style = ""
          document.getElementById("row-"+id).cells[4].children[1].children[0].style = "color:red; cursor:pointer;"
          document.getElementById("row-"+id).cells[4].children[2].style = ""
        }
      }
    }, 'json');
  }
