
let abc

document.getElementById("search-form").addEventListener("submit", async (event) => {
    event.preventDefault();
  
    const query = document.getElementById("search-input").value;
    const response = await fetch(`http://127.0.0.1:8000/search?query=${query}`);
    const responseText = await response.json();
    
    const jsonString = '[' + responseText.replace(/}{/g, '},{') + ']';
    const data = JSON.parse(jsonString);
    console.log(data);
    displayResults(data[0]);
    abc = data[0];
    // console.log(data.Rank);
  });
  
inner_html = ''

results_container = document.getElementById('results_container')

//looping through abc to fill the html_template
displayResults = (abc)=> {
                            for (let i = 0; i < abc.length; i++) {
                                // console.log(i);
                                let inner_data = abc[i];
                                console.log(inner_data[i]);
                                //extrcating data from inner_data
                                let rank = inner_data.rank;
                                // console.log(rank);
                                let url = inner_data.url;
                                let doc_id = inner_data.doc_id;
                                let snippet = inner_data.text;
                                // console.log(snippet);
                                //creating html template
                                html_template = ` 
                                    <div class="sub_results">
                                    <div class="rank_header">
                                            <h3>rank: ${rank} </h3>
                                                <span>
                                                    <select class="rank_dropdown" aria-label="label for the select">
                                                        <option value="0">0</option>
                                                        <option value="1">1</option>
                                                        <option value="2">2</option>
                                                    </select>
                                                </span>
                                        </div>
                                        <h4><a href="${url}" target="_blank">${url}</a></h4>
                                        <p>
                                        ${snippet}
                                        </p>
                                    </div>
                                    `
                                inner_html += html_template
                            }
results_container.innerHTML = inner_html
}


//decorations
document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.rank_dropdown');

    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener('change', () => {
            console.log(`Selected value: ${dropdown.value}`);
        });
    });
});
