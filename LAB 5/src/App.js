import { useState } from 'react';
import './App.css';

function StarRating({ rating, onRate }) {
  return (
    <div style={{ display: 'flex', gap: '4px', cursor: 'pointer' }}>
      {[1, 2, 3, 4, 5].map((star) => (
        <span
          key={star}
          onClick={() => onRate(star)}
          style={{ fontSize: '24px' }}
        >
          {star <= rating ? '⭐' : '☆'}
        </span>
      ))}
    </div>
  );
}

function MovieCard({ movie, onRemove, onUpdateReview, onUpdateRating }) {
  const [review, setReview] = useState(movie.review);
  const [isEditing, setIsEditing] = useState(false);

  function handleSaveReview() {
    onUpdateReview(movie.id, review);
    setIsEditing(false);
  }

  return (
    <div style={{
      background: '#1e1e2e',
      borderRadius: '12px',
      padding: '20px',
      marginBottom: '16px',
      color: '#fff',
      boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0, fontSize: '20px', color: '#e0e0ff' }}>{movie.title}</h3>
        <button
          onClick={() => onRemove(movie.id)}
          style={{
            background: '#ff4d4d',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            padding: '6px 14px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Remove
        </button>
      </div>

      <div style={{ marginTop: '12px' }}>
        <label style={{ fontSize: '14px', color: '#aaa' }}>Rating:</label>
        <StarRating
          rating={movie.rating}
          onRate={(newRating) => onUpdateRating(movie.id, newRating)}
        />
        <div style={{ marginTop: '4px', fontSize: '18px' }}>
          {'⭐'.repeat(movie.rating)}
        </div>
      </div>

      <div style={{ marginTop: '12px' }}>
        <label style={{ fontSize: '14px', color: '#aaa' }}>Review:</label>
        {isEditing ? (
          <div style={{ marginTop: '6px' }}>
            <textarea
              value={review}
              onChange={(e) => setReview(e.target.value)}
              style={{
                width: '100%',
                minHeight: '60px',
                background: '#2a2a3e',
                color: '#fff',
                border: '1px solid #444',
                borderRadius: '8px',
                padding: '8px',
                resize: 'vertical',
                boxSizing: 'border-box'
              }}
            />
            <button
              onClick={handleSaveReview}
              style={{
                marginTop: '6px',
                background: '#4caf50',
                color: '#fff',
                border: 'none',
                borderRadius: '8px',
                padding: '6px 14px',
                cursor: 'pointer'
              }}
            >
              Save
            </button>
          </div>
        ) : (
          <div
            onClick={() => setIsEditing(true)}
            style={{
              marginTop: '6px',
              padding: '8px',
              background: '#2a2a3e',
              borderRadius: '8px',
              cursor: 'pointer',
              minHeight: '40px',
              color: movie.review ? '#fff' : '#666'
            }}
          >
            {movie.review || 'Click to add a review...'}
          </div>
        )}
      </div>
    </div>
  );
}

function AddMovieForm({ onAdd }) {
  const [title, setTitle] = useState('');
  const [rating, setRating] = useState(0);
  const [review, setReview] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    if (!title.trim()) return;
    onAdd({
      id: Date.now(),
      title: title.trim(),
      rating: rating,
      review: review.trim()
    });
    setTitle('');
    setRating(0);
    setReview('');
  }

  return (
    <form onSubmit={handleSubmit} style={{
      background: '#1e1e2e',
      borderRadius: '12px',
      padding: '20px',
      marginBottom: '24px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
    }}>
      <h3 style={{ margin: '0 0 16px 0', color: '#e0e0ff' }}>Add a Movie</h3>

      <input
        type="text"
        placeholder="Movie title..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{
          width: '100%',
          padding: '10px',
          background: '#2a2a3e',
          color: '#fff',
          border: '1px solid #444',
          borderRadius: '8px',
          marginBottom: '12px',
          boxSizing: 'border-box',
          fontSize: '16px'
        }}
      />

      <div style={{ marginBottom: '12px' }}>
        <label style={{ color: '#aaa', fontSize: '14px', marginRight: '8px' }}>Rating:</label>
        <StarRating rating={rating} onRate={setRating} />
      </div>

      <textarea
        placeholder="Write a review..."
        value={review}
        onChange={(e) => setReview(e.target.value)}
        style={{
          width: '100%',
          minHeight: '60px',
          padding: '10px',
          background: '#2a2a3e',
          color: '#fff',
          border: '1px solid #444',
          borderRadius: '8px',
          marginBottom: '12px',
          resize: 'vertical',
          boxSizing: 'border-box',
          fontSize: '14px'
        }}
      />

      <button
        type="submit"
        style={{
          background: '#6c63ff',
          color: '#fff',
          border: 'none',
          borderRadius: '8px',
          padding: '10px 24px',
          cursor: 'pointer',
          fontWeight: 'bold',
          fontSize: '16px'
        }}
      >
        Add Movie
      </button>
    </form>
  );
}

function App() {
  const [movies, setMovies] = useState([]);

  function addMovie(movie) {
    setMovies([...movies, movie]);
  }

  function removeMovie(id) {
    setMovies(movies.filter((m) => m.id !== id));
  }

  function updateReview(id, review) {
    setMovies(movies.map((m) => (m.id === id ? { ...m, review } : m)));
  }

  function updateRating(id, rating) {
    setMovies(movies.map((m) => (m.id === id ? { ...m, rating } : m)));
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: '#121220',
      padding: '40px 20px'
    }}>
      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <h1 style={{ color: '#fff', textAlign: 'center', marginBottom: '8px' }}>
          🎬 Movie Watch List
        </h1>
        <p style={{ color: '#888', textAlign: 'center', marginBottom: '32px' }}>
          Track the movies you watch and rate them
        </p>

        <AddMovieForm onAdd={addMovie} />

        {movies.length === 0 ? (
          <p style={{ color: '#555', textAlign: 'center', marginTop: '40px', fontSize: '18px' }}>
            No movies added yet. Add your first movie above!
          </p>
        ) : (
          <div>
            <h2 style={{ color: '#e0e0ff', marginBottom: '16px' }}>
              Your Movies ({movies.length})
            </h2>
            {movies.map((movie) => (
              <MovieCard
                key={movie.id}
                movie={movie}
                onRemove={removeMovie}
                onUpdateReview={updateReview}
                onUpdateRating={updateRating}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
