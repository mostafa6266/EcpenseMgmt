const searchField  = document.querySelector('#searchField');
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainert = document.querySelector(".pagination-containert");
const tableBody= document.querySelector(".table-body");
const noResults = document.querySelector(".no-results");
tableOutput.style.display = "none";
searchField.addEventListener('keyup', (e)=>{

    const srearchValue = e.target.value;
    tableBody.innerHTML = "" ; 
    if(srearchValue.trim().length > 0){
        paginationContainert.style.display = "none";

        fetch('/search-expenses', {
            body:JSON.stringify({searchText:srearchValue}),
            method:'POST',
        })
        .then((res)=>res.json())
        .then((data)=>{
            console.log('data',data)
            appTable.style.display = "none";
            tableOutput.style.display = "block";
            if(data.length === 0){ 
                noResults.style.display = "block";
                tableOutput.style.display = "none";

            }else{
                noResults.style.display = "none";
                data.forEach(item => {
                    tableBody.innerHTML+=
                `
                <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>`;
                });
                
            }
        });

    }else{
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainert.style.display = "block";
    }
});

