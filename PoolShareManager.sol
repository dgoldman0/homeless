// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title PoolShareManager
 * @notice This contract manages shared liquidity provisioning into Uniswap v4 pools for pairs of PRIME and various tokenA tokens.
 *         Users contribute only tokenA, and the contract supplies a matched value of PRIME from its own reserves, then adds
 *         both tokens to the corresponding Uniswap v4 pool. In return, users receive share credits that represent their proportional
 *         ownership in that pool’s liquidity position. These credits can later be redeemed for a share of the tokenA assets.
 *         Optionally, each pool may have an ERC-20 wrapper contract allowing credit transfers between users.
 *
 * @dev Designed to simplify liquidity contribution by allowing users to provide only tokenA while the contract handles PRIME pairing
 *      and position management through Uniswap v4’s PoolManager. Price alignment is assumed to be handled externally.
 */

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function transferFrom(address sender,address recipient,uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
}

interface IPoolManager {
    struct PoolKey {
        address currency0;
        address currency1;
        uint24 fee;
        int24 tickSpacing;
    }
    function create(PoolKey memory key, bytes32 salt) external returns (address pool);
    function modifyPosition(
        address pool,
        int24 lowerTick,
        int24 upperTick,
        int256 amount0Delta,
        int256 amount1Delta
    ) external returns (uint256 liquidity, uint256 amount0, uint256 amount1);
    function collect(
        address pool,
        address recipient,
        uint128 amount0Requested,
        uint128 amount1Requested
    ) external returns (uint256 amount0, uint256 amount1);
}

contract PoolShareManager {
    /// @notice Token used as the base pair asset for all pools
    address public immutable PRIME;
    /// @notice Uniswap v4 PoolManager address
    address public immutable POOL_MANAGER;
    /// @notice Admin address
    address public owner;

    /// @dev Configuration for each tokenA-based pool
    struct PoolConfig {
        address pool;       // Uniswap v4 pool address
        address wrapper;    // Optional ERC-20 wrapper for transferable credits
        int24   lowerTick;  // Lower tick for the pool position
        int24   upperTick;  // Upper tick for the pool position
    }

    mapping(address => PoolConfig) public pools;      // tokenA => PoolConfig
    mapping(address => mapping(address => uint256)) public credits;    // tokenA => user => credit balance
    mapping(address => uint256)           public totalCredits;         // tokenA => total supply of credits

    event PoolInitialized(address indexed tokenA, address pool);
    event WrapperSet(address indexed tokenA, address wrapper);
    event Deposited(address indexed tokenA, address indexed user, uint256 amountA, uint256 amountP, uint256 delta);
    event Redeemed(address indexed tokenA, address indexed user, uint256 creditBurned, uint256 amountA);
    event TransferManagerSet(address indexed tokenA, address previous, address current);
    event CreditsTransferred(address indexed tokenA, address indexed from, address indexed to, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "PoolShareManager: caller must be owner");
        _;
    }

    constructor(address _prime, address _poolManager) {
        PRIME        = _prime;
        POOL_MANAGER = _poolManager;
        owner        = msg.sender;
    }

    /// @notice Initialize a new Uniswap v4 pool for a given tokenA
    /// @dev Only callable by owner; intended for one-time setup per tokenA
    function initPool(
        address tokenA,
        uint24 fee,
        int24  lowerTick,
        int24  upperTick,
        bytes32 salt
    ) external onlyOwner {
        require(pools[tokenA].pool == address(0), "already initialized");

        IPoolManager.PoolKey memory key = IPoolManager.PoolKey({
            currency0: PRIME,
            currency1: tokenA,
            fee: fee,
            tickSpacing: upperTick - lowerTick > 0 ? uint32(upperTick - lowerTick) : uint32(1)
        });

        address pool = IPoolManager(POOL_MANAGER).create(key, salt);
        pools[tokenA] = PoolConfig({
            pool: pool,
            wrapper: address(0),
            lowerTick: lowerTick,
            upperTick: upperTick
        });
        emit PoolInitialized(tokenA, pool);
    }

    /// @notice Set or update the ERC-20 wrapper for a pool (enabling credit transfers)
    function setWrapper(address tokenA, address wrapper) external onlyOwner {
        address prev = pools[tokenA].wrapper;
        pools[tokenA].wrapper = wrapper;
        emit WrapperSet(tokenA, wrapper);
        emit TransferManagerSet(tokenA, prev, wrapper);
    }

    /// @notice Deposit tokenA; matched with PRIME; credits are minted to sender
    function deposit(address tokenA, uint256 amountA) external {
        PoolConfig memory cfg = pools[tokenA];
        require(cfg.pool != address(0), "PoolShareManager: pool not ready");

        IERC20(tokenA).transferFrom(msg.sender, address(this), amountA);

        uint256 balA = IERC20(tokenA).balanceOf(cfg.pool);
        uint256 balP = IERC20(PRIME).balanceOf(cfg.pool);
        require(balA > 0 && balP > 0, "PoolShareManager: pool empty");
        uint256 amountP = (amountA * balP) / balA;
        require(IERC20(PRIME).balanceOf(address(this)) >= amountP, "insufficient PRIME");

        IERC20(tokenA).approve(POOL_MANAGER, amountA);
        IERC20(PRIME).approve(POOL_MANAGER, amountP);
        IPoolManager(POOL_MANAGER).modifyPosition(
            cfg.pool,
            cfg.lowerTick,
            cfg.upperTick,
            int256(amountP),
            int256(amountA)
        );

        uint256 delta = (amountA * 1e18) / balA;
        credits[tokenA][msg.sender] += delta;
        totalCredits[tokenA]      += delta;

        emit Deposited(tokenA, msg.sender, amountA, amountP, delta);
    }

    /// @notice Burn credits to withdraw proportional share of tokenA from pool
    function burnCredits(address tokenA, uint256 creditAmount) external {
        uint256 userCredit = credits[tokenA][msg.sender];
        require(userCredit >= creditAmount, "PoolShareManager: insufficient credit");
        uint256 total = totalCredits[tokenA];
        require(total > 0, "PoolShareManager: no credits");

        credits[tokenA][msg.sender] -= creditAmount;
        totalCredits[tokenA]        -= creditAmount;

        uint256 share = (creditAmount * 1e18) / total;

        PoolConfig memory cfg = pools[tokenA];
        (uint256 outP, uint256 outA) = IPoolManager(POOL_MANAGER).collect(
            cfg.pool,
            address(this),
            uint128(type(uint256).max),
            uint128(type(uint256).max)
        );

        IERC20(tokenA).transfer(msg.sender, (outA * share) / 1e18);

        emit Redeemed(tokenA, msg.sender, creditAmount, (outA * share) / 1e18);
    }

    /// @notice Called by wrapper to transfer credits between users
    function transferCredits(
        address tokenA,
        address from,
        address to,
        uint256 amount
    ) external {
        require(msg.sender == pools[tokenA].wrapper, "PoolShareManager: forbidden");
        uint256 bal = credits[tokenA][from];
        require(bal >= amount, "PoolShareManager: insufficient");
        credits[tokenA][from] -= amount;
        credits[tokenA][to]   += amount;
        emit CreditsTransferred(tokenA, from, to, amount);
    }

    /// @notice Transfer contract ownership
    function transferOwnership(address newOwner) external onlyOwner {
        owner = newOwner;
    }
}
