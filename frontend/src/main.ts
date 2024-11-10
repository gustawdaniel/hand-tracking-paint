import './style.css'
import { setupSSEReceiver } from './sse.ts'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
     <p id="sse"></p>
  </div>
`

setupSSEReceiver(document.querySelector<HTMLElement>('#sse')!)
