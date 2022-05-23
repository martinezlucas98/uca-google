import SearchBar from '../../components/SearchBar/SearchBar';
import Show_results from '../../components/Results/Show-results';
import styles from '../../styles/results.module.css'
import UcaLogo from '../../components/UcaLogo/UcaLogo'


function results({data}) {
 
  return(
    
    <div className={styles.wrapper}>
      {/* <div className={styles.logo}>
        <UcaLogo/>
      </div> */}
     
      <div className={styles.search_bar}>
        <SearchBar/>
        
      </div>

      <div className={styles.results}>
        <Show_results datox={data}/>
       
      </div>

     
    </div>
    
    
  );
}

// This gets called on every request
export async function getServerSideProps({query}) {
  // Fetch data from external API
  
  console.log(query.q)
  //const res = await fetch('http://127.0.0.1:8000/search?q=' + query.q)
  //let data = await res.json()
  let data =
    {"status": "success",
      "time": 0.8,
      "results":[
        {
        "title": "Algun titulo del html",
        "url": 'https://name.com',
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text                   ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged"
        },
        {
          "title": "Algun titulo del html1",
          "url": 'https://name.com',
          "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text                   ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged"
        },
        {
          "title": "Algun titulo del html2",
          "url": 'https://name.com',
          "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text                   ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged"
        }
      ]
    }
  
  console.log(query)
  //data = JSON.parse(data);
  console.log(data)
  //console.log(typeof data)
  // Pass data to the page via props

  return { props: { data } }
}

export default results;