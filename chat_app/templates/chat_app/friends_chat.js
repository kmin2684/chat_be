// section toggle
function friends_room_toggle(event) {
    if (event.target.className==="section_friend") {
        view_on(vertical_list_friends, true);
        view_on(vertical_list_groups, false);
    }
    if (event.target.className==="section_groups") {
        view_on(vertical_list_friends, false);
        view_on(vertical_list_groups, true);  
    }
}

function view_on(elem, state) {
    state? elem.style.display = 'initial' : elem.style.display = 'none'; 
}

const section_friend = document.querySelector('.section_friend');
const section_groups = document.querySelector('.section_groups');
const vertical_list_friends = document.querySelector('.vertical_list_friends');
const vertical_list_groups = document.querySelector('.vertical_list_groups');

section_friend.addEventListener("click", friends_room_toggle);
section_groups.addEventListener("click", friends_room_toggle);


// load window(conversation, new chat form, etc)
// this should close every other windows


// add event listener to every group
//     first test with console.log
[...document.querySelectorAll(".friend")].map(x => x.addEventListener('click', load_conversation));

// load chat 
function load_conversation (event) {
    console.log(event.target.innerHTML.trim());
}