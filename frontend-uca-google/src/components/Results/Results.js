import styles from './Results.module.css';
function Results(props){

  return(
    <div className={styles.container}>
      <div className='wrapper'>
        <p className={styles.link}> Link = {props.link}</p>
        <p className={styles.description}> Descripcion = {props.description}</p>
      </div>

    </div>

  );
}

export default Results;

