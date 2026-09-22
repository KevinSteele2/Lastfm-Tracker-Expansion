import { useState, useEffect, useRef } from 'react'

function App() {
  const [imageUrl, setImageUrl] = useState('')
  const [breedId, setBreedId] = useState(null)
  const [aliases, setAliases] = useState([])
  const [guess, setGuess] = useState('')
  const [message, setMessage] = useState('')
  const [streak, setStreak] = useState(0)
  const [showInput, setShowInput] = useState(true)
  const inputRef = useRef(null)

  function loadNewDog() {
    setMessage('')
    setGuess('')
    setShowInput(true)

    fetch('/api/dogbreed/random')
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          setMessage(data.error)
          return
        }
        setBreedId(data.breed_id)
        setAliases(data.aliases || [])
        setImageUrl(data.image_url)
        inputRef.current?.focus()
      })
  }

  useEffect(() => {
    loadNewDog()
  }, [])

  function submitGuess() {
    if (!guess || !breedId) {
      return
    }

    fetch('/api/dogbreed/guess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ breed_id: breedId, guess: guess, aliases: aliases })
    })
      .then(response => response.json())
      .then(data => {
        if (data.correct) {
          setStreak(s => s + 1)
          setMessage(`Correct! It's a ${data.answer}.`)
        } else {
          setStreak(0)
          setMessage(`Nope, that was a ${data.answer}.`)
        }

        setShowInput(false)
        setTimeout(loadNewDog, 2000)
      })
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter') {
      submitGuess()
    }
  }

  return (
  <div className="text-center font-sans">
    <a href="/" className="block text-left px-4 pt-4">&lt; Back</a>

    <h1 className="font-serif font-normal text-3xl border-b border-gray-400 pb-2 mx-4">
      Dog Breed Guesser
    </h1>

    <p className="mt-4">Streak: <span>{streak}</span></p>

    <div className="my-4">
      <img src={imageUrl} alt="Guess the breed" className="max-w-[400px] mx-auto" />
    </div>

    {showInput && (
      <div className="my-4">
        <input
          ref={inputRef}
          type="text"
          value={guess}
          onChange={e => setGuess(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a breed name..."
          className="border border-gray-400 rounded px-2 py-1"
        />
        <button onClick={submitGuess} className="ml-2 px-3 py-1 border rounded hover:bg-gray-100">
          Guess
        </button>
      </div>
    )}

    <p className="my-4">{message}</p>
  </div>
)
}

export default App