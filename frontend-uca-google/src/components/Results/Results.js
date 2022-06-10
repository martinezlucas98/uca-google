
import styles from './Results.module.css';
import Link from 'next/link';
//Usamos esta funcion para truncar la "descripcion", en el caso de que sea muy larga
function truncateString(str, num){
  if(str != null){
    if(str.length > num){
      return str.slice(0, num) + "...";
    }else{
      return str;
    }
  }
 
}
function Results(props){

  return(
    <Link href={props.link} passHref>
      <a>
    
          <div className={styles.container}>
                
                <div className={styles.wrapper}>

                  <p className={styles.title}> Title = {props.title}</p>
                  <p className={styles.link}> Link = {props.link}</p>
                  <p className={styles.description}> Descripcion = {truncateString(props.description, 20)}</p>
                
                </div>
          
          </div>
        </a>
      </Link>
    
   

  );
}




export default Results;

