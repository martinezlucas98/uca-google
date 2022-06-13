import SearchBar from '../../components/SearchBar/SearchBar';
import Show_results from '../../components/Results/Show-results';
import styles from '../../styles/results.module.css'
import UcaLogo from '../../components/UcaLogo/UcaLogo'
import { COOKIE_NAME_PRERENDER_BYPASS } from 'next/dist/server/api-utils';


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
 

  console.log('query: ', query.input)
  const res = await fetch('http://127.0.0.1:8000/search?q=' + query.input)
  let data = await res.json()
  // for(let i=0;i<10000;i++){
  //   console.log(i);

  // }

  //  let data =
  //    {"status": "success",
  //      "time": 0.8,
  //      "results":[
  //        {
  //        "title": "Algun titulo del html",
  //        "url": 'https://name.com',
  //        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text                   ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged"
  //        },
  //        {
  //          "title": "Algun titulo del html1",
  //          "url": 'https://name.com',
  //          "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text                   ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged"
  //        },
  //        {
  //          "title": "Algun titulo del html2",
  //          "url": 'https://name.com',
  //          "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text                   ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged"
  //        }
  //      ]
  //    }
  
  console.log(query)
  data = JSON.parse(data);
  console.log(data)
  
  
  return { props: { data } }
}

export default results;