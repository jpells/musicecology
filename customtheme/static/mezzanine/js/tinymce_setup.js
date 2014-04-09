
function CustomFileBrowser(field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        file: window.__filebrowser_url + '?pop=2&type=' + type,
        width: 820,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "yes",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no"
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId
    });
    return false;
}

if (typeof tinyMCE != 'undefined') {

    tinyMCE.init({

        // main settings
        mode : "specific_textareas",
        editor_selector : "mceEditor",
        theme: "advanced",
        language: "en",
        dialog_type: "window",
        editor_deselector : "mceNoEditor",

        // general settings
        width: '700',
        height: '350',
        indentation : '10px',
        fix_list_elements : true,
        remove_script_host : true,
        accessibility_warnings : false,
        object_resizing: false,
        //cleanup: false, // SETTING THIS TO FALSE WILL BREAK EMBEDDING YOUTUBE VIDEOS
        forced_root_block: "p",
        remove_trailing_nbsp: true,

	content_css : "/static/css/mezzanine.css,/static/css/cartridge.css,/static/css/bootstrap_bootswatch_slate.css,/static/css/custom.css",

        external_link_list_url: '/displayable_links.js',
        relative_urls: false,
        convert_urls: false,

        // callbackss
        file_browser_callback: "CustomFileBrowser",

        // theme_advanced
        theme_advanced_toolbar_location: "top",
        theme_advanced_toolbar_align: "left",
        theme_advanced_statusbar_location: "",
        theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
        theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
        theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
        theme_advanced_buttons4 : "insertlayer,moveforward,movebackward,absolute,|,styleprops,spellchecker,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,template,blockquote,pagebreak,|,insertfile,insertimage",
        theme_advanced_path: false,
        theme_advanced_blockformats: "p,h1,h2,h3,h4,pre",
        theme_advanced_styles: "[all] clearfix=clearfix;[p] small=small;[img] Image left-aligned=img_left;[img] Image left-aligned (nospace)=img_left_nospacetop;[img] Image right-aligned=img_right;[img] Image right-aligned (nospace)=img_right_nospacetop;[img] Image Block=img_block;[img] Image Block (nospace)=img_block_nospacetop;[div] column span-2=column span-2;[div] column span-4=column span-4;[div] column span-8=column span-8",
        theme_advanced_resizing : true,
        theme_advanced_resize_horizontal : false,
        theme_advanced_resizing_use_cookie : true,
        theme_advanced_styles: "Image left-aligned=img_left;Image left-aligned (nospace)=img_left_nospacetop;Image right-aligned=img_right;Image right-aligned (nospace)=img_right_nospacetop;Image Block=img_block",
        advlink_styles: "intern=internal;extern=external",

        // plugins
	plugins : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
        advimage_update_dimensions_onchange: true,

        // remove MS Word's inline styles when copying and pasting.
        //paste_remove_spans: true,
        //paste_auto_cleanup_on_paste : true,
        //paste_remove_styles: true,
        //paste_remove_styles_if_webkit: true,
        //paste_strip_class_attributes: true,

        // don't strip anything since this is handled by bleach
        valid_elements: "+*[*]",
        valid_children: "+button[a]"

	});

}

