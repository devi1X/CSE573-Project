
var num=1;


var dropdown_sort_html = 
'<span margin-top:20px;" id="num-of-results"></span>' +
'<div class="dropdown" id="sorting-dropdown" style="padding-bottom: 10px;">'+
    '<button id="sort-btn" class="btn dropdown-toggle" style="font-size:16px;" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-top:0px;">' +
    'Sort Condition</button>'+
    '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton" style="font-size:16px;">' +
        '<a class="dropdown-item" href="#" onclick="sort_by_time_newest_first()">Sort by Time (Newest first)</a>'+
        '<a class="dropdown-item" href="#" onclick="sort_by_time_oldest_first()">Sort by Time (Oldest first)</a>'+
        '<a class="dropdown-item" href="#" onclick="sort_by_correction_strongest_first()">Sort by Correlation (Strongest first)</a>'+
    '</div>'+
'</div>';







updateData(data_arr);





$(document).ready(function(){
    $(document).on('change', 'input[name="filterItem"]', function(e) {
                
    var checked_filters = [];

    $('input[name="filterItem"]:checked').each(function() {
        checked_filters.push(this.value);
    });
        // console.log($('input[name="filterItem"]:checked').val());
        console.log(checked_filters);


        document.getElementById("searchResults").innerHTML = '<div style="font-size: 16px; color: #bdbdbd;">' + 
                                                dropdown_sort_html +
                                                '</div>';
       

        

        var result_cnt = 0;

        for (var i = 0; i < data_arr.length; i ++) {

          if ((checked_filters.includes(data_arr[i]['post_Time_ym'])) || (checked_filters.length == 0)) {


                  result_cnt += 1;

 
                  var postHeading = data_arr[i].title;
                  var postTime = data_arr[i].post_Time;
                  var author = data_arr[i].author;
                  var postContent = data_arr[i].content;
                  var postTag = "";
                  var postLink = data_arr[i].link;

                  for (var j = 0; j < data_arr[i].preferred_name_list.length; j ++) {
                      postTag += data_arr[i].preferred_name_list[j];
                      cur_unique_tags.push(data_arr[i].preferred_name_list[j]);
                      if (j != data_arr[i].preferred_name_list.length - 1) {
                          postTag += ", ";
                      }
                  }
  
                  var card_html = 
                  '<div class="card">' +
                  '<a target="_blank" rel="noopener noreferrer" href="' + postLink + '">'+
                  '<h5 class="card-header search-keyword" style="font-size:18px;">Title: ' + postHeading + '</h5>' +
                  '</a>' +
                  '<div class="card-body">' +
                  '<h5 class="card-title">Post Time: ' + postTime + '</h5>' +
                  '<h5 class="card-title">Author: ' + author + '</h5>' +
                  '<p class="card-text">' + postContent + '</h5>' +
                  '<p class="card-title" style="font-size:15px; color:rgba(158,202,225,1);">Tags: ' + postTag + '</p>' +
                  // '<h5 class="card-title"><a target="_blank" rel="noopener noreferrer" href="' + postLink + '">Click to see the original post</a>' + '</h5>' +
                  //   '<p class="card-text">' + postLink + '</p>' +
                  '</div>' +
              '</div>';

                  
                  document.getElementById("searchResults").innerHTML += card_html;
              
          }
        }

        document.getElementById("num-of-results").innerHTML = result_cnt + " results";
        document.getElementById("searchResults").style.display = 'block';
    });








});



var cur_unique_tags = [];
var cur_search_txt = document.getElementById('searchingInput').value;

function search() {
  var cur_search_txt = document.getElementById('searchingInput').value;
  var startTime = new Date();
  $.ajax({
    url: "/searchResultPage",
    type: "GET",
    async: false,
    data: {
        // searchTerm:cur_search_txt,
        startTime:startTime.toString(),
    }
});
  window.location.href = `/searchResultPage?searchTerm=${cur_search_txt}`;
  // window.location.href = `/searchResultPage`;

  
  // updateData(data_arr);

}





function updateData(data) {
  document.getElementById("filters").innerHTML = '<p style="font-size:20px">Time Period</p>'
    cur_unique_tags = [];
    document.getElementById("searchResults").innerHTML = '<div style="font-size: 16px; color: #bdbdbd;">' + 
                                                dropdown_sort_html +
                                                '</div>';
       

    // document.getElementById("searchResults").innerHTML = '<div style="font-size: 16px; color: #bdbdbd;"><span id="num-of-results"></span> results </div>'; 
    var cur_search_txt = document.getElementById('searchingInput').value;
    var result_cnt = 0;

    // console.log("length here")
    // console.log(data.length)

    for (var i = 0; i < data.length; i ++) {
 
          // result_cnt += 1;

          var postHeading = data[i].title;
          var postTime = data[i].post_Time;
          var author = data[i].author;
          var postContent = data[i].content;
          var postTag = "";
          var postLink = data[i].link;

          for (var j = 0; j < data[i].preferred_name_list.length; j ++) {
              postTag += data[i].preferred_name_list[j];
              cur_unique_tags.push(data[i].preferred_name_list[j]);
              if (j != data[i].preferred_name_list.length - 1) {
                  postTag += ", ";
              }
          }

          var card_html = 
                      '<div class="card">' +
                      '<a target="_blank" rel="noopener noreferrer" href="' + postLink + '">'+
                      '<h5 class="card-header search-keyword" style="font-size:18px;">Title: ' + postHeading + '</h5>' +
                      '</a>' +
                      '<div class="card-body">' +
                      '<h5 class="card-title">Post Time: ' + postTime + '</h5>' +
                      '<h5 class="card-title">Author: ' + author + '</h5>' +
                      '<p class="card-text">' + postContent + '</h5>' +
                      '<p class="card-title" style="font-size:15px; color:rgba(158,202,225,1);">Tags: ' + postTag + '</p>' +
                      // '<h5 class="card-title"><a href="' + postLink + '">Click to see the original post</a>' + '</h5>' +
                      //   '<p class="card-text">' + postLink + '</p>' +
                      '</div>' +
                  '</div>';

            
          document.getElementById("searchResults").innerHTML += card_html;
      
    }

    document.getElementById("num-of-results").innerHTML = data_arr.length + " results";
    if(data_arr.length != 0) {
      document.getElementById("searchResults").style.display = 'block';


      // cur_unique_tags = [...new Set(cur_unique_tags)];
      for (var i = 0; i < cur_month_list.length; i ++) {
          filter_item = cur_month_list[i];
          var filter_item_html = 
              '<input class="check-filter" type="checkbox" name="filterItem" id="' + 
              filter_item + 
              '" value="' + 
              filter_item + 
              '"  />&nbsp;<label for="' 
              + filter_item + 
              '">' + 
              filter_item + 
              '</label><br />';
              document.getElementById("filters").innerHTML += filter_item_html;
      }
    }
}






function sort_by_time_newest_first() {
  var data_arr_sorted = data_arr.sort(function(a, b) {
    
    var keyA = new Date(a.post_Time),
      keyB = new Date(b.post_Time);
    // Compare the 2 dates
    if (keyA < keyB) return 1;
    if (keyA > keyB) return -1;
    return 0;
  });
  updateData(data_arr_sorted);
  document.getElementById('sort-btn').innerHTML = "Sort by Time (Newest first)";

}


function sort_by_time_oldest_first() {
  
  var data_arr_sorted = data_arr.sort(function(a, b) {
    var keyA = new Date(a.post_Time),
      keyB = new Date(b.post_Time);
    // Compare the 2 dates
    if (keyA < keyB) return -1;
    if (keyA > keyB) return 1;
    return 0;
  });
  updateData(data_arr_sorted);
  document.getElementById('sort-btn').innerHTML = "Sort by Time (Oldest first)";
}



function sort_by_correction_strongest_first() {
  
  var data_arr_sorted = data_arr.sort(function(a, b) {
    var keyA = a.cur_search_name_score,
      keyB = b.cur_search_name_score;
    // Compare the 2 dates
    if (keyA < keyB) return 1;
    if (keyA > keyB) return -1;
    return 0;
  });
  updateData(data_arr_sorted);
  document.getElementById('sort-btn').innerHTML = "Sort by Correlation (Strongest first)";
}