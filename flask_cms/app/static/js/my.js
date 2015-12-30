function addCarouselImageField(){
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $("#carouselImageWrapper"); //Fields wrapper
    var carouselImageCount = $("#carouselImageWrapper #carouselImage").length;
    var csrf_token_name = "images-" + carouselImageCount + "-csrf_token"
    var image_link_name = "images-" + carouselImageCount +"-image_link"
    var image_caption_name = "images-" + carouselImageCount +"-image_caption"
    var image_description_name = "images-" + carouselImageCount +"-image_description"

    $(wrapper).append('<div id="carouselImage">\
        <hr class="col-sm-10">\
        <div class="col-sm-10">\
            <a role="button" id="addCarouselFieldButton" class="btn btn-sm btn-danger pull-right" onclick="javascript:removeCarouselImageField($(this))"><span class="glyphicon glyphicon-minus"></span></a>\
        </div>\
        <div style="display:none;"><input id='+csrf_token_name+' name='+csrf_token_name+' type="hidden" value="None"></div>\
        <div class="form-group">\
            <div class="col-sm-10">\
                <label for='+image_link_name+'>Image Link</label>:\
                <input autofocus="" class="form-control" id='+image_link_name+' name='+image_link_name+' required="" type="text" value="">\
            </div>\
        </div>\
        <div class="form-group">\
            <div class="col-sm-10">\
                <label for='+image_caption_name+'>Caption</label>:\
                <input autofocus="" class="form-control" id='+image_caption_name+' name='+image_caption_name+' required="" type="text" value="">\
            </div>\
        </div>\
        <div class="form-group">\
            <div class="col-sm-10">\
                <label for='+image_description_name+'>Description</label>:\
                <input autofocus="" class="form-control" id='+image_description_name+' name='+image_description_name+' required="" type="text" value="">\
            </div>\
        </div>\
    </div>'); //add input box
};

function removeCarouselImageField(elem){
    elem.parent('div').parent('div').remove();
};

function replaceWidgetForm(widget_type){
   $.get("/admin/widget", { type: widget_type })
       .done(function(data){
       $("#widgetForm").replaceWith(data);
       });
};