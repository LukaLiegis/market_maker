use tokio_tungstenite::{connect_async, tungstenite::protocol::Message};
use futures_util::{SinkExt, StreamExt};
use serde_json::json;
use url::Url;
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
struct OrderBookEntry {
    price: String,
    size: String,
}

#[derive(Debug, Deserialize, Serialize)]
struct OrderBookData {
    s: String,
    b: Vec<OrderBookEntry>,
    a: Vec<OrderBookEntry>,
    u: u64,
    seq: u64,
}

#[derive(Debug, Deserialize, Serialize)]
struct WebSocketResponse {
    topic: String,
    #[serde(rename = "type")]
    response_type: String,
    data: OrderBookData,
    ts: u64,
}

#[tokio::main]
async fn main() {
    if let Err(e) = run().await {
        eprintln!("Error: {}", e);
    }
}

async fn run() -> Result<(), Box<dyn std::error::Error>> {
    let url = Url::parse("wss://stream-testnet.bybit.com/v5/public/linear")?;

    let (ws_stream, _) = connect_async(url).await?;
    println!("WebSocket connected");

    let (mut write, mut read) = ws_stream.split();

    let subscribe_msg = json!({
        "op": "subscribe",
        "args": ["orderbook.1.BTCUSDT"]
    });
    write.send(Message::Text(subscribe_msg.to_string())).await?;

    while let Some(message) = read.next().await {
        match message {
            Ok(Message::Text(text)) => {
                match serde_json::from_str::<WebSocketResponse>(&text) {
                    Ok(response) => {
                        println!("Received orderbook update:");
                        println!("Symbol: {}", response.data.s);
                        println!("Timestamp: {}", response.ts);
                        println!("Bids:");
                        for bid in response.data.b.iter().take(5) {
                            println!("  Price: {}, Size: {}", bid.price, bid.size);
                        }
                        println!("Asks:");
                        for ask in response.data.a.iter().take(5) {
                            println!("  Price: {}, Size: {}", ask.price, ask.size);
                        }
                    },
                    Err(e) => println!("Failed to parse JSON: {}", e),
                }
            }
            Ok(_) => {}
            Err(e) => return Err(e.into()),
        }
    }

    Ok(())
}