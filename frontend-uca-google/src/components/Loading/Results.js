
import styles from './Results.module.css';
import Link from 'next/link';
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
//Usamos esta funcion para truncar la "descripcion", en el caso de que sea muy larga

function Results(props){

  return(
   
      <div className={styles.container}>
            
            <div style={{marginLeft:20, marginTop:10, marginBottom:20}}>
          
             
              <Skeleton height={40} width={200} style={{marginBottom:10}}/>
              <Skeleton height={20} width={300} style={{marginBottom:10}}/>
              <Skeleton count={3} width={500}/>

            </div>
      
      </div>
      
     
    
   

  );
}




export default Results;

