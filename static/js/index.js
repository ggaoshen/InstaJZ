
function error_cb(error) { /* print error msg */
    console.log(error);
}

/*
 *
 *    Likes
 *
 */

function create_like(success_cb, error_cb) { /* cb=callback */
    var post_pk = $(this).siblings('.hidden-data').find('.post-pk').text(); /* get post's pk from page: this = the list where submit-like is found on, find its sibling (other divisions on same level) with .hidden-data, find post-pk in its child*/
    console.log(post_pk);

    $.ajax({ /* send a small request, no redirect to different page */
        type: "POST",
        url: '/insta/like',
        data: { /* send post_pk as data */
            post_pk: post_pk
        },
        success: function(data) { success_cb(data); }, /*  success_cb calls like_update_view function */
        error: function(error) { error_cb(error); }
    });
}
  
function like_update_view(data) {
    console.log(data);

    // toggle heart
    var $hiddenData = $('.hidden-data.' + data.post_pk); /* this is hidden-data1, hidden-data2, ..., specify pk*/
    if (data.result) {
      $hiddenData.siblings('.submit-like').removeClass('fa-heart-o').addClass('fa-heart');
    } else {
      $hiddenData.siblings('.submit-like').removeClass('fa-heart').addClass('fa-heart-o');
    }
  
    // update like count
    var difference = data.result ? 1 : -1; // if data.results=1, then 1, else -1
    var $post = $('.view-update.' + data.post_pk); // find where post pk is on index page
    var $likes = $post.find('.likes'); // go to class=likes division on index page
    var likes = parseInt($likes.text()); // get likes division text and grab the integer from this text
    likes = likes + difference;
  
    console.log('likes', likes);
  
    if (likes == null || isNaN(likes)) { // this means no likes before, likes=null+1=null. hardcode as 1 like
      $likes.text('1 like');
    } else if (likes === 0) { // means it had 1 like before, likes=1-1=0, hardcode as empty
      $likes.text('');
    } else if (likes === 1) { // could be 0 or 2 before. regardless, hardcode as 1 like
      $likes.text('1 like');
    } else {
      $likes.text(likes + ' likes'); // other like counts, just use likes as is
    }
}
 
$('.submit-like').on('click', function() { /* search for all html files with class name submit-like, trigger function when clicked */
    create_like.call(this, like_update_view, error_cb); /* create like(success_cb=like_update_view, error_cb=error_cb) */
});

  
/*
*
*    Comments
*
*/
  
function enterPressed(e) {
    if (e.key === "Enter") { return true; }
    return false;
}
   
function validComment(text) {
    if (text == '') return false;
    return true;
}
  
function create_comment(success_cb, error_cb) {
    var comment_text = $(this).val();
    var post_pk = $(this).parent().siblings('.hidden-data').find('.post-pk').text();
  
    console.log(comment_text, post_pk);
  
    $.ajax({
      type: "POST",
      url: '/insta/comment',
      data: {
        comment_text: comment_text,
        post_pk: post_pk
      },
      success: function(data) { success_cb(data); },
      error: function(error) { error_cb(error); }
    });
}

function comment_update_view(data) {
    console.log(data);
    var $post = $('.hidden-data.' + data.post_pk);
    var commentHTML = '<li class="comment-list__comment"><a class="user"> ' + data.commenter_info.username + '</a> <span class="comment">'
                    + data.commenter_info.comment_text +'</span></li>'
  
    $post.closest('.view-update').find('.comment-list').append(commentHTML);
  }
  
  $('.add-comment').on('keyup', function(e) {
    if (enterPressed(e)) {
      if (validComment($(this).val())) {
        create_comment.call(this, comment_update_view, error_cb);
        $(this).val('');
      }
    }
  });
  

/*
 *
 *    Follow/Unfollow
 *
 */

function follow_user(success_cb, error_cb, type) {
    var follow_user_pk = $(this).attr('id');
    console.log(follow_user_pk);
  
    $.ajax({
      type: "POST",
      url: '/insta/togglefollow',
      data: {
        follow_user_pk: follow_user_pk,
        type: type
      },
      success: function(data) { success_cb(data); },
      error: function(error) { error_cb(error); }
    });
}
  
function update_follow_view(data) {
    console.log('calling update_follow_view');
    console.log('data',data);
    var $button = $('.follow-toggle__container .btn');
    $button.addClass('unfollow-user').removeClass('follow-user');
    $button.text('Unfollow');

    var $span = $('.follower_count');
    var span_text = parseInt(document.getElementById("follower_id").innerText);
    $span.text(span_text + 1);
}

function update_unfollow_view(data) {
    console.log('calling update_unfollow_view');
    console.log('data',data);
    var $button = $('.follow-toggle__container .btn');
    $button.addClass('follow-user').removeClass('unfollow-user');
    $button.text('Follow');

    var $span = $('.follower_count');
    var span_text = parseInt(document.getElementById("follower_id").innerText);
    $span.text(span_text - 1);
}


$('.follow-toggle__container').on('click', '.follow-user', function() {
    follow_user.call(this, update_follow_view, error_cb, 'follow');
});

$('.follow-toggle__container').on('click', '.unfollow-user', function() {
    follow_user.call(this, update_unfollow_view, error_cb, 'unfollow');
});